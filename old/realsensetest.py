## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

###############################################
##      Open CV and Numpy integration        ##
###############################################

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

try:
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # For each depth coordinate, calculate the theta
        depth_thcopy=np.arange(np.shape(depth_image)[1]) * 0.04
        depth_thcopy=np.tile(depth_thcopy,(np.shape(depth_image)[0],1))
        print (np.shape(depth_thcopy))
        print (np.shape(depth_image))

        # For each depth coordinate, calculate the r
        depth_rcopy=np.copy(depth_image).astype("float")
        depth_rcopy=np.square(depth_rcopy)
        depth_rcopy-=0.5
        depth_rcopy=np.sqrt(depth_rcopy)
        
        # Map the image to theta / r coordinates
        flat=np.zeros(np.size(depth_image))
        for i,v in enumerate(depth_rcopy):
            for j,r in enumerate(v):
                theta=depth_thcopy[i,j]
                try:
                    flat[np.floor(r*np.cos(theta)),np.floor(r*np.sin(theta))]=color_image[i,j]
                except IndexError:
                    pass
        # Display
        cv2.imshow('fimg',flat)
        cv2.waitKey(1)

finally:

    # Stop streaming
    pipeline.stop()