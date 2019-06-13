import pyrealsense2 as rs
import numpy as np
import cv2
import math
import serialtest as st
import see_plus_plus as spp

# Configure depth and color streams
# Create a pipeline
pipeline = rs.pipeline()

#Create a config and configure the pipeline to stream
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 360, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 360, rs.format.bgr8, 30)

# Start streaming
profile = pipeline.start(config)

# Getting the depth sensor's depth scale (see rs-align example for explanation)
#Also sets up clipping_distance
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
clipping_distance = 3 / depth_scale

#Upper and lower bounds for the lines of tape
b_lower = (90, 100, 100)
b_upper = (110,255,200)

y_lower = (25, 150, 100)
y_upper = (30,255,255)

#:reps the aligning
align_to = rs.stream.color
align = rs.align(align_to)
angle_buf = []

#High/low speed for the car
low_speed = 1510
high_speed = 1585

#Sets the starting speed, this hardly lasts, because it gets overwritten very quickly
#st.move(str(int(1565)))

try:
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()
        if not color_frame:
            continue

        #Aligns the colour frame to the depth frame, not really in use atm
        aligned_frames = align.process(frames)
        aligned_depth_frame = aligned_frames.get_depth_frame()
        
        #Converts the raw frame data into np arrays
        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        #Applies a blur to the image, probs should change this to use c2 at some point
        color_image = cv2.blur(color_image,(3,3))
        
        #Creates a copy of the color image, which we draw a bunch of stuff on. 
        c2 = color_image.copy()

        depth_image_3d = np.dstack((depth_image,depth_image,depth_image)) #depth image is 1 channel, color is 3 channels

        
        #This line removes all pixels out of a set distance, not really in use.
        #c2 = np.where((depth_image_3d > clipping_distance) | (depth_image_3d <= 0), 153, c2)
       
        #Crops the top half of the image
        c2 = c2[160:320, 0:640]

        #Converts the remaining image from RGB to HSV
        hsv = cv2.cvtColor(c2, cv2.COLOR_BGR2HSV)

        #Creates masks, and then applies those masks to the image.
        y_mask = cv2.inRange(hsv, y_lower, y_upper)
        b_mask = cv2.inRange(hsv, b_lower, b_upper)
        y_result = cv2.bitwise_and(hsv, hsv, mask=y_mask)
        b_result = cv2.bitwise_and(hsv, hsv, mask=b_mask)

        #Runs canny edge detection on the remaining images, not really in use, but useful for some stuff
        y_edges = cv2.Canny(y_result, 300, 200)
        b_edges = cv2.Canny(b_result, 300, 200)

        #Combines the edges
        edges = cv2.addWeighted(y_edges, 1, b_edges, 1, 1)

        #Some setup for hough_lines late on, once again, not in use atm, but could be very useful for corner/straight detection.
        minLineLength = 100
        maxLineGap = 10

        y_lines = cv2.HoughLinesP(y_edges, 1, np.pi/180, 40, minLineLength=minLineLength, maxLineGap=maxLineGap)
        b_lines = cv2.HoughLinesP(b_edges, 1, np.pi/180, 30, minLineLength=minLineLength, maxLineGap=maxLineGap)

        #Finds contours in our individual images. This is what we actually use to determine our 2 points of interest.
        #hierarchy isn't in use, but if its not there, the function doesn't work.
        b_contours, hierarchy = cv2.findContours(cv2.cvtColor(b_result, cv2.COLOR_BGR2GRAY), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        y_contours, hierarchy = cv2.findContours(cv2.cvtColor(y_result, cv2.COLOR_BGR2GRAY), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        ##################################################################################################################
        #The below is no longer in use, but it is what we used to determine where the lines are. It doesn't work spectacularly well, but could come in handy later.
        
        # depth_intrin = depth_frame.profile.as_video_stream_profile().intrinsics
        # y_deg = 0
        # x_deg = 0
        # try:
        #     a = None
        #     c = 100000
        #     for a in y_lines:
        #         for x1,y1,x2,y2 in a:
        #             if y1 < c:
        #                 c = y1
        #                 a = b
        #             #cv2.line(c2,(x1,y1),(x2,y2),(0,255,0),2)
        #     for x1,y1,x2,y2 in a:
        #         #cv2.line(c2,(x1,y1),(x2,y2),(0,0,255),2)
        #         angle = math.atan2( (y2 - y1), (x2 - x1))
        #         y_deg = math.degrees(angle)    
        # except:
        #     print("No yellow")

        # try:
        #     a = None
        #     c = 0
        #     for b in b_lines:
        #         for x1,y1,x2,y2 in b:
        #             if y1 > c:
        #                 c = x1
        #                 a = b
        #             #cv2.line(c2,(x1,y1),(x2,y2),(0,255,0),2)
        #     for x1,y1,x2,y2 in a:
        #         #\cv2.line(c2,(x1,y1),(x2,y2),(0,0,255),2)
        #         angle = math.atan2((y2 - y1), (x2 - x1))
        #         x_deg = math.degrees(angle)    
        # except:
        #     print("No blue")

        # if x_deg is not 0 and y_deg is not 0:
        #     angle_buf.append((y_deg+x_deg)/2)
        #     if len(angle_buf) > 20:
        #         angle_buf.pop(0)


        ########################################################################################
        # This is the actually important stuff. 
        # The code below finds the lowest point in contours (by y value of the pixel) on each image (yellow/blue).
        # Also draws them
        # This could use some improvment.


        b_y = -1

        if(b_contours):
            lowest_point = 0
            p = -1
            q = -1
            for i in range(len(b_contours)):
                if len(b_contours[i]) < 20:
                    continue
                for f in range(len(b_contours[i])):
                    if b_contours[i][f][0][1] > lowest_point:
                        lowest_point = b_contours[i][f][0][1]
                        p = i
                        q = f

            cv2.circle(c2, (b_contours[p][q][0][0], b_contours[p][q][0][1]), 4, (0, 255, 255))
            b_y = b_contours[p][q][0][1]
        
        y_y = -1
        
        if(y_contours):
            lowest_point = 0
            p = -1
            q = -1
            for i in range(len(y_contours)):
                if len(y_contours[i]) < 20:
                    continue
                for f in range(len(y_contours[i])):
                    if y_contours[i][f][0][1] > lowest_point:
                        lowest_point = y_contours[i][f][0][1]
                        p = i
                        q = f

            cv2.circle(c2, (y_contours[p][q][0][0], y_contours[p][q][0][1]), 4, (255, 0, 255))
            y_y = y_contours[p][q][0][1]

        ########################################################################################
        # This is the part where we actually decide things.
        
        # Simply subtracts the height of the blue pixel from the yellow pixel.
        # Multiplier is arbitrary.
        temp = (b_y - y_y) * 0.3

        # Centers the difference on 90 degrees
        angle = 90 - temp

        #Full lock cases.
        if angle > 135:
            angle = 135
        elif angle < 45:
            angle = 45

        # Very rudimentary straightness formula, but basically, the more straight the wheels are, the more zoom zoom
        # This is not great, as we need to slow before we start turning, and start speeding up when straightening.
        straightness = 1 - (abs(angle-90) / 45)
        speed = low_speed + (high_speed - low_speed) * straightness
        
        #This is for safety, should never actually be invoked.
        if speed > high_speed:
            speed = high_speed
        elif speed < low_speed:
            speed = low_speed

        st.move(str(int(round(angle))))
        st.move(str(1565))

        #If we can't see either line, don't move.
        #This is rudimentary and needs work.
       # if b_y == -1 and y_y == -1:
       ##     pass
       #     st.move(str(1650))
       # else:
       #     st.move(str(int(round(speed))))

        # Show various images, don't uncomment these when this is on the board, as it has a headless version of opencv, and doesn't suppport them.
        # Uncomment waitKey when you're using these.
        # The best ones to show are ('Color', c2) and ('Edges', edges) 

        #cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        #cv2.imshow('Edges', edges)
        cv2.imshow('Color', c2)
        #cv2.imshow('mask', o)
        #cv2.imshow('asdd', depth_colormap)
        cv2.waitKey(1)

finally:

    # Stop streaming
    pipeline.stop() 
