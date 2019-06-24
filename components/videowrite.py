import cv2
import numpy as np
 
debugVid=None
origVid=None
# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.

def writeToFile(helper):
    global debugVid
    global origVid
    if debugVid is None:
        frame_width=helper['draw_image'].shape[1]
        frame_height=helper['draw_image'].shape[0]
        debugVid = cv2.VideoWriter('debug.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
    if origVid is None:
        frame_width=helper['image'].shape[1]
        frame_height=helper['image'].shape[0]
        origVid = cv2.VideoWriter('original.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
    debugVid.write(helper['draw_image'])
    origVid.write(helper['image'])

import atexit
def close(): 
    global debugVid
    global origVid
    debugVid.release()
    origVid.release()
atexit.register(close)