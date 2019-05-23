import pyrealsense2 as rs
import numpy as np
import cv2

# Configure depth and color streams
# Create a pipeline
pipeline = rs.pipeline()

#Create a config and configure the pipeline to stream
#  different resolutions of color and depth streams
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
# Start streaming
profile = pipeline.start(config)

# Getting the depth sensor's depth scale (see rs-align example for explanation)
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()

# Start streaming

im = cv2.imread('image.png')

lower = (90, 0, 0)
upper = (120,255,255)

align_to = rs.stream.color
align = rs.align(align_to)

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
    

        
        depth_image_3d = np.dstack((depth_image,depth_image,depth_image)) #depth image is 1 channel, color is 3 channels
        
        hsv = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, lower, upper)
        o = cv2.bitwise_and(hsv, hsv, mask=mask)
        grey_color = 153

        edges = cv2.Canny(color_image, 500, 200)

        bg_removed = np.where((o < 10), grey_color, depth_image_3d)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(bg_removed, alpha=0.1), cv2.COLORMAP_JET)

        contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #a = cv2.applyColorMap(cv2.convertScaleAbs(contours, alpha=0.3), cv2.COLORMAP_JET)

        depth_intrin = depth_frame.profile.as_video_stream_profile().intrinsics

        c2 = color_image.copy()

        #if(contours):
        #    for c in range(len(contours)):
        #        print(c)
        #        for (x, y) in contours[c].reshape(-1,2):
        #            cv2.circle(c2, (x, y), 1, (0, 40 * c, 0), 3)
    
        # Show images
        #cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('Edges', edges)
        #cv2.imshow('Color', c2)
        #cv2.imshow('mask', o)
        #cv2.imshow('asdd', depth_colormap)
        cv2.waitKey(1)

finally:

    # Stop streaming
    pipeline.stop() 
