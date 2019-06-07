import pyrealsense2 as rs
import numpy as np
import cv2
import math
import serialtest as st

# Configure depth and color streams
# Create a pipeline
pipeline = rs.pipeline()

#Create a config and configure the pipeline to stream
#  different resolutions of color and depth streams
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 360, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 360, rs.format.bgr8, 30)
# Start streaming
profile = pipeline.start(config)

# Getting the depth sensor's depth scale (see rs-align example for explanation)
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
clipping_distance = 3 / depth_scale
# Start streaming
b_lower = (100, 100, 100)
b_upper = (110,255,200)

y_lower = (25, 50, 100)
y_upper = (30,255,255)

align_to = rs.stream.color
align = rs.align(align_to)
angle_buf = []

low_speed = 1570
high_speed = 1590

st.move(str(1575))
try:
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()
        if not color_frame:
            continue

        aligned_frames = align.process(frames)
        aligned_depth_frame = aligned_frames.get_depth_frame()
        depth_image = np.asanyarray(aligned_depth_frame.get_data())


        color_image = np.asanyarray(color_frame.get_data())
    

        color_image = cv2.blur(color_image,(3,3))
        
        c2 = color_image.copy()
        depth_image_3d = np.dstack((depth_image,depth_image,depth_image)) #depth image is 1 channel, color is 3 channels
        #c2 = np.where((depth_image_3d > clipping_distance) | (depth_image_3d <= 0), 153, c2)
       
        c2 = c2[160:320, 0:640]

        hsv = cv2.cvtColor(c2, cv2.COLOR_BGR2HSV)

        y_mask = cv2.inRange(hsv, y_lower, y_upper)
        b_mask = cv2.inRange(hsv, b_lower, b_upper)
        y_result = cv2.bitwise_and(hsv, hsv, mask=y_mask)
        b_result = cv2.bitwise_and(hsv, hsv, mask=b_mask)
        grey_color = 153

        y_edges = cv2.Canny(y_result, 300, 200)
        b_edges = cv2.Canny(b_result, 300, 200)

        minLineLength = 100
        maxLineGap = 10


        y_lines = cv2.HoughLinesP(y_edges, 1, np.pi/180, 40, minLineLength=minLineLength, maxLineGap=maxLineGap)
        b_lines = cv2.HoughLinesP(b_edges, 1, np.pi/180, 30, minLineLength=minLineLength, maxLineGap=maxLineGap)

        edges = cv2.addWeighted(y_edges, 1, b_edges, 1, 1)
         
        b_contours, hierarchy = cv2.findContours(cv2.cvtColor(b_result, cv2.COLOR_BGR2GRAY), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        y_contours, hierarchy = cv2.findContours(cv2.cvtColor(y_result, cv2.COLOR_BGR2GRAY), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #a = cv2.applyColorMap(cv2.convertScaleAbs(contours, alpha=0.3), cv2.COLORMAP_JET)

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
                
        temp = (b_y - y_y) * 0.3

        angle = 90 - temp

        if angle > 135:
            angle = 135
        elif angle < 45:
            angle = 45

        angle += 3

        straightness = 1 - (abs(angle-90) / 45)
        speed = low_speed + (high_speed - low_speed) * straightness


        st.move(str(int(round(angle))))
        #st.move(str(speed))
    
        # Show images
        #cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        #cv2.imshow('Edges', edges)
#        cv2.imshow('Color', c2)
        #cv2.imshow('mask', o)
        #cv2.imshow('asdd', depth_colormap)
#        cv2.waitKey(1)

finally:

    # Stop streaming
    pipeline.stop() 
