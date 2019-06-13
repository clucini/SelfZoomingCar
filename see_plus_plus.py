import components.seefoward as camera
import components.pathfinder as pathfinder
import components.localiser as localiser
import components.getCorrection as getCorrection
import components.actOn as actOn

def reciever(image):
    # determine path to be followed in our coordinate frame
    pathToFollow = pathfinder.getPathToFollow(image)
    # determine our location in our coordinate frame
    ourLocation = localiser.getOurLocation(image)
    # calculate any corrections
    correction = getCorrection(ourLocation, pathToFollow)
    # physically adjust course, speed etc
    actOn.do(correction)


# The main loop starts in topdown.
# We implement a function that is passed to topdown; topdown
# runs this at each loop when it gets the corresponding image.
camera.sendImageTo(reciever)

# Start the program
camera.start()