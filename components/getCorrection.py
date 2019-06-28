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

    temp = (helper['b_y'] - helper['y_y'])

    # Centers the difference on 90 degrees
    angle = 90 + temp

    #Full lock cases.
    if angle > 135:
        angle = 135

    elif angle < 45:
        angle = 45
    helper['correction']=np.clip(angle,45,135)
    
    print('ANGLE:::::::::::', angle)
    center = helper['ourLocation']
    length = 100
    x =  int((center[0]) + length * -np.cos(angle * 3.1415 / 180.0))
    y =  int((center[1]) + length * -np.sin(angle * 3.1415 / 180.0))
    cv2.line(helper['draw_image'], tuple(center), (x,y), (255,255,255), thickness=3)

    return

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


