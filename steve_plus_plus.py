import components.seeforward as camera
import components.nullPathFinder as pathfinder
import components.obstacledetector as obstacleDetector
import components.localiser as localiser
import components.getCorrection as gc
import components.actOnfake as actOn
import cv2

def reciever(image):
    # determine path to be followed in our coordinate frame
    pathToFollow, yellowpoints, bluepoints = pathfinder.getPathToFollow(image)
    # determine a new path to follow taking into account obstacles
    pathToFollow = obstacleDetector.amendPath(pathToFollow,image)
    # determine our location in our coordinate frame
    ourLocation = localiser.getOurLocation(image)
    # calculate any corrections
    if pathToFollow is None:
        if not (yellowpoints or bluepoints):
            print('c')
            actOn.move(1500)
        elif not yellowpoints:
            print('a')
            actOn.move(45)
        elif not bluepoints:
            print('b')
            actOn.move(135)
        else:
            print("uhoh")
    else:
        correction = gc.getCorrection(ourLocation, pathToFollow)
        actOn.move(int(correction)) # physically adjust course, speed etc
        for e in pathToFollow:
            cv2.circle(image, (int(e[0]), int(e[1])), 4, (0, 0, 255))
    cv2.imshow("Color", image)
    cv2.waitKey(1)


# The main loop starts in topdown.
# We implement a function that is passed to topdown; topdown
# runs this at each loop when it gets the corresponding image.
camera.sendImageTo(reciever)

# Start the program
camera.start()