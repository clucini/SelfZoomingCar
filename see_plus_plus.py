import components.seeforward as camera
import components.linearPathFinder as pathfinder
import components.localiser as localiser
import components.getCorrection as gc
import components.actOnLnx as actOn
import cv2

def reciever(image):
    # determine path to be followed in our coordinate frame
    pathToFollow, yellowpoints, bluepoints = pathfinder.getPathToFollow(image)
    # determine our location in our coordinate frame
    ourLocation = localiser.getOurLocation(image)
    # calculate any corrections
    if pathToFollow is None:
        if yellowpoints is not None:
            actOn.move(135)
        else:
            actOn.move(45)
    else:
        correction = gc.getCorrection(ourLocation, pathToFollow)
        print(correction)
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