import components.seeforward as camera
import components.quickLinearPathFinder as pathfinder
import components.obstacleDetector as obstacleDetector
import components.localiser as localiser
import components.getCorrection as gc
import components.actOn as actOn
import components.getContours as getContours
import cv2

def reciever(image):
    #Get Contours
    helper = {}
    helper['image'] = image
    getContours.get_c(helper)
    if helper['main_y_contour'] is None and helper['main_b_contour'] is None:
        actOn.move(1500)
        print('Can\' see anything')
    elif helper['main_y_contour'] is None:
        actOn.move(45)
        print('Can\'t see yellow')
    elif helper['main_b_contour'] is None:
        actOn.move(135)
        print('Can\'t see blue')
    else:
        # determine path to be followed in our coordinate frame
        pathfinder.getPathToFollow(helper)
        # determine a new path to follow taking into account obstacles
        obstacleDetector.amendPath(helper)
        # determine our location in our coordinate frame
        localiser.getOurLocation(helper)
        # calculate any corrections
        correction = gc.getCorrection(helper)
        actOn.move(int(correction)) # physically adjust course, speed etc
        for e in helper['midpoints']:
            cv2.circle(image, (int(e[0]), int(e[1])), 4, (0, 0, 255))
    
    cv2.imshow("Color", image)
    cv2.waitKey(1)


# The main loop starts in topdown.
# We implement a function that is passed to topdown; topdown
# runs this at each loop when it gets the corresponding image.
camera.sendImageTo(reciever)

# Start the program
camera.start()