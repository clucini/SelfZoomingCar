import numpy as np
import cv2

# FUNCTION getCorrection(helper)
# gets the difference between the two edge points and gives us the line in the middle



def getCorrection(helper):
    ourLocation = helper['ourLocation']
    pathToFollow = helper['midpoints']
    image = helper['image']

    # Trim based on path
    radius=5
    minDist=10000

    #just to initialise
    targetPoint=ourLocation
    centre=np.array((0,1))

    # when there is no midpoint set to go straight
    if pathToFollow is None:
        helper['correction']=90
        return

    #
    for i in pathToFollow:
        dist=np.linalg.norm(i-ourLocation)
        if dist>radius and dist<minDist:
            targetPoint=i
            mindist=dist
    deviationVector=targetPoint-ourLocation
    deviationVector[1]*=-1
    angle = int(np.arctan2(deviationVector[1], deviationVector[0])*180/np.pi)
    angle = 90 - ((90 - angle) * 2)
    if not image is None and helper['debug']:
        helper['draw_image']=cv2.line(helper['draw_image'],tuple(ourLocation.astype(int)),tuple(targetPoint.astype(int)),(255,255,255),10)
    helper['correction']=np.clip(angle,45,135)

if __name__=="__main__":
    helper = {}
    helper['ourLocation'] = [100,0]
    helper['midpoints'] = [4,2,1,10]
    helper['image'] = 0
    print(getCorrection(np.array((320,100))))


