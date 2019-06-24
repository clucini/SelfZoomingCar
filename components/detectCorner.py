import pyrealsense2 as rs
import numpy as np
import cv2
import math

# FUNCTION
# Corner detect



def detectCorner(helper):
    
    # get values from helper 
    currMidpoint = helper['midpoints']
    # image = helper['image']

    angleList = []
    angleAvg = 0
    inc = 0

    for i in currMidpoint[:-1]:
         
        # gets the distance from the edge to the centre through line algorithm
        rise = currMidpoint[inc+1][1] - i[1]
        run = currMidpoint[inc+1][0] - i[0]

        if rise < 0:
            negativeRiseFlag = 1
            print('Going back')
        else: 
            print('Going forward')
        if run < 0:
            negativeRunFlag = 1
            print('Going Left')
        else:
            print('Going Right')
        
        

        angle = math.atan(rise/run)
        angleList.append(angle)
        # print('This is angle: ')
        # print(angle)

    angleAvg = np.mean(angleList)
    # print('AVERAGE ANGLE: ')
    # print(angleAvg)

    inc += 1
    

    return angleAvg

# INCOMPLETE



# interpret what the angle gives us
# def cornerAction(helper):
#     angleList









# def inCorner(helper):
    
#     # converts the remaining image from rgb to hsv
#     hsv = helper['hsv']

#     # threshold out obstables
#     obj_lower = (150, 60, 60)
#     obj_upper = (170,255,255)
#     obj_mask = cv2.inRange(hsv, obj_lower, obj_upper)

#     # get contours
#     # MORE LIKE FIND CORNER

#     # if no corners, break

#     # draw corners on image

#     # find the lowest set of points in the approximation

#     # find the blue and yellow corresponding poitns
#     blue_contours=helper['main_b_contour']
#     yellow_contours=helper['main_y_contour']
#     if not blue_contours is None:
#         bluepair=find_overlaps(np.array([minpts[0]]),blue_contours)[0]
#         bluedist=np.linalg.norm(bluepair[0]-bluepair[1])
#         blueresult=((bluepair[0]+bluepair[1])/2).astype(int)
#     else:
#         bluedist=0
#     if not yellow_contours is None:
#         yellopair=find_overlaps(np.array([minpts[0]]),yellow_contours)[0]
#         yellodist=np.linalg.norm(yellopair[0]-yellopair[1])
#         yelloresult=((yellopair[0]+yellopair[1])/2).astype(int)
#     else:
#         yellodist=0

#     # find the distance between blues and yellows and choose one    
#     if bluedist<yellodist:
#         result=yelloresult
#     else:
#         result=blueresult

#     helper['midpoints'] = [result]
