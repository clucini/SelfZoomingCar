import components.seeforward as camera
import components.quickLinearPathFinder as pathfinder
import components.nullObstacleDetector as obstacleDetector
import components.localiser as localiser
import components.getCorrection as gc
import components.actOn as actOn
import components.getContours as getContours
import cv2

def reciever(image):
    #Get Contours
    main_y_contour, main_b_contour = getContours.get_c(image) 
    if not (main_y_contour or main_b_contour):
        actOn.move(1500)
        print('Can\' see anything')
    elif not main_y_contour:
        actOn.move(45)
        print('Can\'t see yellow')
    elif not main_b_contour:
        act0n.move()
        print('Can\'t see blue')
    else:
        # determine path to be followed in our coordinate frame
        pathToFollow, yellowpoints, bluepoints = pathfinder.getPathToFollow(main_y_contour, main_b_contour)
        # determine a new path to follow taking into account obstacles
        pathToFollow = obstacleDetector.amendPath(pathToFollow,image)
        # determine our location in our coordinate frame
        ourLocation = localiser.getOurLocation(image)
        # calculate any corrections
        correction = gc.getCorrection(ourLocation, pathToFollow, image)
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