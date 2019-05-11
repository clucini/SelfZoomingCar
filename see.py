import pyrealsense2 as rs
import numpy as np
import cv2

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

im = cv2.imread('image.png')

lower = (90, 0, 0)
upper = (120,255,255)

try:
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue

        # Convert images to numpy arrays
        color_image = np.asanyarray(color_frame.get_data())
    

        #hsv_blue = cv2.cvtColor((0,0,255), cv2.COLOR_BGR2HSV)
        hsv = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

        edges = cv2.Canny(hsv, 500, 450)

        

        mask = cv2.inRange(hsv, lower, upper)
        #o = cv2.bitwise_and(hsv, hsv, mask=mask)

        # Show images
        #cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('Edges', edges)
        cv2.imshow('Color', color_image)
        cv2.imshow('mask', mask)
        #cv2.imshow('asdd', t)
        cv2.waitKey(1)

finally:

    # Stop streaming
    pipeline.stop() 
