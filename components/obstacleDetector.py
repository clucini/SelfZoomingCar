import cv2
import numpy as np

# TODO: 
# if the obstacle is outside the track.

def find_overlaps(y_contours, b_contours):

    y_contours=y_contours[y_contours[:,1].argsort()]
    b_contours=b_contours[b_contours[:,1].argsort()]

    y_counter = 0
    b_counter = 0

    pairs = []

    for i in range(0, len(y_contours)):
        lastdiff = 100000
        f = 0
        if i % 20 != 0:
            continue
        while abs(y_contours[i][1] - b_contours[f][1]) <= lastdiff:
            lastdiff = abs(y_contours[i][1] - b_contours[f][1])
            f += 1
            if f >= len(b_contours):
                break


        # if lastdiff < 5:
        pairs.append((y_contours[i],b_contours[f-1]))

    return pairs








def amendPath(helper):
    # Converts the remaining image from RGB to HSV
    hsv=helper['hsv']
    # threshold out obstacles
    obj_lower = (150, 60, 60)
    obj_upper = (170,255,255)
    obj_mask = cv2.inRange(hsv, obj_lower, obj_upper)
    # Get contours
    cnts=cv2.findContours(obj_mask,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)[0]
    # get contour with largest area
    la=0
    laobj=None
    for i in cnts:
        ca=cv2.contourArea(i)
        if ca>la:
            laobj=i
            la=ca
    # if no obstacles, break
    if laobj is None or la<40:
        return
    # Approximate contour to square
    epsilon = 0.1*cv2.arcLength(laobj,True)
    approx = cv2.approxPolyDP(laobj,epsilon,True)
    # Draw contours on image
    drawImg=helper['draw_image']
    drawImg=cv2.drawContours(drawImg,[approx],-1,(255,0,0),-1)
    # Find the lowest set of points in the approximation
    ys=approx[:,:,1].reshape((approx.shape[0]))
    mins=ys.argsort()[-2:]
    minpts=approx[mins,:,:].reshape((2,2))
    xs=minpts[:,0].reshape((minpts.shape[0]))
    mins=xs.argsort()
    minpts=minpts[mins]
    # Find blue and yellow corresponding points.
    blue_contours=helper['main_b_contour']
    yellow_contours=helper['main_y_contour']
    bluepair=find_overlaps(np.array([minpts[0]]),blue_contours)[0]
    yellopair=find_overlaps(np.array([minpts[1]]),yellow_contours)[0]
    # find the distance between blues and yellows and choose one
    bluedist=np.linalg.norm(bluepair[0]-bluepair[1])
    yellodist=np.linalg.norm(yellopair[0]-yellopair[1])
    result=((bluepair[0]+bluepair[1])/2).astype(int)
    if bluedist<yellodist:
        result=((yellopair[0]+yellopair[1])/2).astype(int)
    helper['midpoints']=[result]
    
    cv2.circle(drawImg,tuple(result),20,(0,255,255),-1)
    return