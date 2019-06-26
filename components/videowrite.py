import cv2
import numpy as np
import os
 
debugVid=None
origVid=None
# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
num_files = len(os.listdir('vids')) / 2

def writeToFile(helper):
    global debugVid
    global origVid
    # make the directory if it does not exist
    if not (os.path.exists("vids")):
        os.mkdir("vids")
    if debugVid is None:
        frame_width=helper['draw_image'].shape[1]
        frame_height=helper['draw_image'].shape[0]
        debugVid = cv2.VideoWriter('vids/debug'+str(int(num_files))+'.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
    if origVid is None:
        frame_width=helper['image'].shape[1]
        frame_height=helper['image'].shape[0]
        origVid = cv2.VideoWriter('vids/original'+str(int(num_files))+'.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
    debugVid.write(helper['draw_image'])
    origVid.write(helper['image'])

import atexit
def close(): 
    global debugVid
    global origVid
    if not debugVid is None:
        debugVid.release()
    if not origVid is None:
        origVid.release()
atexit.register(close)