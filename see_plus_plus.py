import traceback
import components.seeforward as camera
import components.localiser as localiser
import components.getCorrection as gc
import components.obstacleDetector as obstacleDetector
import components.quickLinearPathFinder as pathfinder
import components.actOnMux as actOn
import components.followLine as followLine
import components.getContours as getContours
import components.clean_contours as cc
import components.get_corner as gCorner
import components.videowrite as videowriter
import components.detectCorner as detectCorner
import cv2
import numpy as np

def reciever(image):
    helper = {}
    helper['image'] = image
    helper['draw_image'] = image.copy()

    localiser.getOurLocation(helper)
    #Get Contours
    getContours.get_c(helper)
    cc.clean(helper)

    if helper['main_y_contour'] is None and helper['main_b_contour'] is None:
        ## this doesnt quite work
        actOn.move(1500)
        helper['midpoints'] = np.array([[0,image.shape[1]/2]])
        print('Can\'t see anything')
    elif helper['main_y_contour'] is None:
        followLine.follow(helper,'blue')
        helper['midpoints'] = np.array([[0,image.shape[1]]])
        print('Can\'t see yellow')
    elif helper['main_b_contour'] is None:
        followLine.follow(helper,'yellow')
        helper['midpoints'] = np.array([[0,0]])
        print('Can\'t see blue')
    else:
        pathfinder.getPathToFollow(helper)    # determine path to be followed in our coordinate frame
        print('Normal operation')
    
    if not helper['midpoints'] is None:
        print("everything is ok")
        # determine a new path to follow taking into account obstacles
        obstacleDetector.amendPath(helper)

        # determine our location in our coordinate frame

        # calculate any corrections
        gc.getCorrection(helper)

        # physically adjust course, speed etc
        gCorner.get_corner(helper)
        actOn.move(int(helper['correction']))
        #Draw things for debug purposes
        for e in helper['midpoints']:
            cv2.circle(helper['draw_image'], (int(e[0]), int(e[1])), 4, (0, 255, 0))

    else:
        actOn.move(90)
    cv2.imshow("uneditted", image)
    cv2.imshow("drawn", helper['draw_image'])
    videowriter.writeToFile(helper)
    if cv2.waitKey(1) == 'q':
        return -1
    else:
         return 0
    return 0


# The main loop starts in topdown.
# We implement a function that is passed to topdown; topdown
# runs this at each loop when it gets the corresponding image.
camera.sendImageTo(reciever)

# Start the program
try:
    camera.start()
    videowriter.close()
except Exception as e:
    print(e)
    traceback.print_exc()
    videowriter.close()


## TODO:
# Stop when no lines detected
