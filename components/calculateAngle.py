import numpy as np
import cv2

# FUNCTION getCorrection(helper)
# gets the difference between the two edge points and gives us the line in the middle



def c(helper):
    ourLocation = helper['ourLocation']
    targetPoint = helper['targetPoint']
    image = helper['image']
    deviationVector=targetPoint-ourLocation
    deviationVector[1]*=-1
    angle = int(np.arctan2(deviationVector[1], deviationVector[0])*180/np.pi)
    angle = 90 - ((90 - angle) * 2)
    if not image is None and helper['debug']:
        helper['draw_image']=cv2.line(helper['draw_image'],tuple(ourLocation.astype(int)),tuple(targetPoint.astype(int)),(255,255,255),10)
    helper['angle']=np.clip(angle,45,135)

if __name__=="__main__":
    helper = {}
    helper['ourLocation'] = np.array([100,0])
    helper['targetPoint'] = np.array([4,2])
    helper['image'] = 0
    helper['debug']=False
    print(c(helper))


