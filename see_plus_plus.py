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
import components.fpsCounter as fps
import cv2
import numpy as np
import os
import time
from threading import Thread

memory = {}
memory['reverse'] = 0
memory['debug'] = True
# read the env file if it exists and if it is live, then don't debug
print("huh")
# try:
#     with open('env', 'r') as fh:
#         whereamI = fh.readline()
#         if "live" in whereamI:
#             print("env with live...")
#             memory['debug'] = False
#         else:
#             print(whereamI)
#         # Store configuration file values
# except FileNotFoundError:
#     print("no env...")
#     pass
    # Keep preset values
memory['time']=time.time()
memory['minfps']=100
memory['totfps']=0
memory['itercount']=0
memory['angle'] = 90
memory['speed'] = 1500
memory['running'] = True

actOnProcess = Thread(target = actOn.move, args=(memory,))

def reciever(helper):
    global memory
    helper['speed'] = 1590
    helper['correction'] = 90
    helper['debug'] = memory['debug']
    image = helper['image']
    helper['draw_image'] = image.copy()
    localiser.getOurLocation(helper)

    width = helper['ourLocation'][0].astype(int)*2
    height = helper['ourLocation'][1].astype(int)
    image[int(height/10*7.5):,\
            int(width/4):int(width/6*5)] = 0
    
    fps.show(memory)

    # Get Contours
    getContours.get_c(helper)
    #cc.clean(helper)
    """ 
    if memory['reverse'] < 0:
        memory['reverse'] += 1
    elif memory['reverse'] > 0:
        helper['speed'] = 1400
        helper['correction'] = memory['lastAngle']
        memory['reverse'] -= 1
        return
    """
    
    if helper['main_y_contour'] is None and helper['main_b_contour'] is None:
        # Be careful
        helper['midpoints'] = None
        helper['speed'] = 1420
        memory['reverse'] -= 5
        if memory['reverse'] < -20:
            memory['reverse'] = 20
    elif helper['main_y_contour'] is None:
        helper['midpoints'] = np.array([[0, image.shape[1]]])
        #followLine.follow(helper, 'blue')
        print('Can\'t see yellow')
    elif helper['main_b_contour'] is None:
        helper['midpoints'] = np.array([[0, 0]])
        #followLine.follow(helper, 'yellow')
        print('Can\'t see blue')
    else:
        # determine path to be followed in our coordinate frame
        pathfinder.getPathToFollow(helper)
        # print('Normal operation')
    if not helper['midpoints'] is None:
        # print("everything is ok")

        # determine a new path to follow taking into account obstacles
        if not obstacleDetector.amendPath(helper) :
            gc.getCorrection(helper)
        # determine our location in our coordinate frame

        # calculate any corrections
        

        # detecting corner: gives which direction we are headed in and prints the angle
        if helper['main_y_contour'] is not None and helper['main_b_contour'] is not None:
            pass
            # print(detectCorner.detectCorner(helper))

        # physically adjust course, speed etc
        # gCorner.get_corner(helper)          # draws a white line
        # Draw things for debug purposes
        if helper['debug']:
            for e in helper['midpoints']:
                cv2.circle(helper['draw_image'],
                           (int(e[0]), int(e[1])), 4, (0, 0, 255))
    memory['angle'] = helper['correction']
    if (memory['debug']):
        # display on the image
        cv2.imshow("uneditted", image)
        cv2.imshow("drawn", helper['draw_image'])
        videowriter.writeToFile(helper)

        # exit image (doesnt work)
        if cv2.waitKey(1) == 'q':
            return -1
        else:
            return 0
        return 0


# The main loop starts in topdown.
# We implement a function that is passed to topdown; topdown
# runs this at each loop when it gets the corresponding image.
camera.sendImageTo(reciever)


# TODO:
# Stop when no lines detected

if __name__ == '__main__':
    actOnProcess.start()

    try:
        camera.start()
    except Exception as e:
        print(e)
        traceback.print_exc()

    finally:
        print('asakjshdakjshdkjahdskjahdshasdfahjafs')
        memory['running']=False
        actOnProcess.join()