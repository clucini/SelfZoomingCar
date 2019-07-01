import numpy as np
import cv2

# FUNCTION getCorrection(helper)
# gets the difference between the two edge points and gives us the line in the middle



def s(helper):
    ourLocation = helper['ourLocation']
    image = helper['image']

    temp = (helper['b_y'] - helper['y_y']) *  0.3

    # Centers the difference on 90 degrees
    angle = 90 - temp

    #Full lock cases.
    if angle > 135:
        angle = 135

    elif angle < 45:
        angle = 45
    helper['angle']=np.clip(angle,45,135)
    
    # print('ANGLE:::::::::::', angle)
    center = helper['ourLocation']
    length = 100
    x =  int((center[0]) + length * -np.cos(angle * 3.1415 / 180.0))
    y =  int((center[1]) + length * -np.sin(angle * 3.1415 / 180.0))
    if helper['debug']:
        cv2.line(helper['draw_image'], tuple(center), (x,y), (255,255,255), thickness=3)

    return