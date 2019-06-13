import pyrealsense2 as rs
import numpy as np
import cv2
import math

# Configure depth and color streams
# Create a pipeline
pipeline = rs.pipeline()

#Create a config and configure the pipeline to stream
config = rs.config()
config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 360, rs.format.bgr8, 30)

# Start streaming
profile = pipeline.start(config)

func_to_send_to = None

def sendImageTo(func):
    global func_to_send_to
    func_to_send_to = func

def start():
    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()
        if not color_frame:
            continue

        #Converts the raw frame data into np arrays
        color_image = np.asanyarray(color_frame.get_data())

        #Applies a blur to the image, probs should change this to use c2 at some point
        color_image = cv2.blur(color_image,(3,3))
        
        #Creates a copy of the color image, which we draw a bunch of stuff on. 
        c2 = color_image.copy()

        #Crops the top half of the image
        # c2 = c2[160:320, 0:640]
        func_to_send_to(c2)
        #cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        #cv2.imshow('Edges', edges)
        #cv2.imshow('mask', o)
        #cv2.imshow('asdd', depth_colormap)

    pipeline.stop() 
