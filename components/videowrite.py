import cv2
import numpy as np
 
out=None
# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.

def writeToFile(helper):
    global out
    if out is None:
        frame_width=helper['draw_image'].shape[1]
        frame_height=helper['draw_image'].shape[0]
        out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
    out.write(helper['draw_image'])

import atexit
def close(): 
    global out
    out.release()
atexit.register(close)