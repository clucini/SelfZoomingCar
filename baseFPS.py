import traceback
import components.seeforward as camera
import components.localiser as localiser
import components.getCorrection as gc
import components.obstacleDetector as obstacleDetector
import components.quickLinearPathFinder as pathfinder
import components.actOnMux as actOn
import components.followGradient as followLine
import components.getContours as getContours
import components.clean_contours as cc
import components.get_corner as gCorner
import components.videowrite as videowriter
import components.detectCorner as detectCorner
import cv2
import numpy as np
import os
import time


memory = {}
memory['reverse'] = 0
memory['debug'] = True
# read the env file if it exists and if it is live, then don't debug
print("huh")
try:
    with open('env', 'r') as fh:
        whereamI = fh.readline()
        if whereamI == "live":
            memory['debug'] = False
        else:
            print(whereamI)
        # Store configuration file values
except FileNotFoundError:
    print("no env...")
    pass
    # Keep preset values
memory['time']=time.time()
memory['minfps']=100
memory['totfps']=0
memory['itercount']=0
def reciever(helper):
    global memory
    helper['speed'] = 1590
    helper['correction'] = 90
    helper['debug'] = memory['debug']
    image = helper['image']
    if helper['debug']:
        helper['draw_image'] = image.copy()
    fps=1/(time.time()-memory['time'])
    print ("FPS:{0}".format(fps))
    if fps<memory['minfps']:
        memory['minfps']=fps
    print ("minFPS:{0}".format(memory['minfps']))
    memory['itercount']+=1;
    memory['totfps']+=fps
    print("avgfps:{0}".format(memory['totfps']/memory['itercount']))
    memory['time']=time.time()
    cv2.imshow('image', helper['image'])
    cv2.waitKey(1)


# The main loop starts in topdown.
# We implement a function that is passed to topdown; topdown
# runs this at each loop when it gets the corresponding image.
camera.sendImageTo(reciever)

# Start the program
try:
    camera.start()
#    videowriter.close()
except Exception as e:
    print(e)
    traceback.print_exc()
#    videowriter.close()


# TODO:
# Stop when no lines detected
