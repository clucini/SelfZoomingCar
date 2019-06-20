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








def amendPath(path,image):
    # Converts the remaining image from RGB to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # threshold out obstacles
    obj_lower = (150, 70, 60)
    obj_upper = (170,255,255)
    obj_mask = cv2.inRange(hsv, obj_lower, obj_upper)
    # Get contours
    cnts=cv2.findContours(obj_mask,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)[0]
    # get contour with largest area
    la=0
    laobj=None
    for i in cnts:
        ca=cv2.contourArea(i)
        if ca>100 and ca>la:
            laobj=i
            la=ca
    # if no obstacles, break
    if laobj is None:
        return path
    # Approximate contour to square
    epsilon = 0.1*cv2.arcLength(laobj,True)
    approx = cv2.approxPolyDP(laobj,epsilon,True)
    # Find the lowest set of points in the approximation
    image=cv2.drawContours(image,[approx],-1,(255,0,0),-1)
    ys=approx[:,:,1].reshape((approx.shape[0]))
    mins=ys.argsort()[-2:]
    print (mins)
    print (approx)
    minpts=approx[mins,:,:].reshape((2,2))
    print(minpts)
    # Draw a line from edge to edge
    m=(minpts[0,1]-minpts[1,1])/(minpts[0,0]-minpts[1,0])
    # TODO FIX INFINITY
    if (minpts[0,0]-minpts[1,0])==0:
        return path
    b=minpts[0,1]-m*minpts[0,0]
    leftborderpoint=[0,int(b)]
    rightborderpoint=[image.shape[1],int(m*image.shape[1]+b)]
    line=np.zeros(image.shape[:2])
    line=cv2.line(line,tuple(leftborderpoint),tuple(rightborderpoint),255,2)
    image=cv2.line(image,tuple(leftborderpoint),tuple(rightborderpoint),255,2)
    # bitwise and it with our yellow and blue contours
    # Upper and lower bounds for the lines of tape (thanks claudio)
    b_lower = (100, 80, 80)
    b_upper = (110,255,200)

    y_lower = (20, 50, 100)
    y_upper = (35,255,255)

    # Get blue and yellow sections (thanks claudio)
    y_mask = cv2.inRange(hsv, y_lower, y_upper)
    b_mask = cv2.inRange(hsv, b_lower, b_upper)
    kernel=(5,5)
    y_mask=cv2.erode(y_mask,kernel);
    b_mask=cv2.erode(b_mask,kernel)

    y_band = np.bitwise_and(y_mask.astype(int),line.astype(int))
    cv2.imshow("line",line)
    cv2.imshow("purey",y_mask)
    cv2.imshow("pureb",b_mask)
    firstNonzero=np.transpose(np.array(np.nonzero(y_band)))
    if len(firstNonzero):
        firstNonzero=firstNonzero[0]
    else:
        return path
    cv2.circle(image,tuple(firstNonzero),20,(0,255,255),-1)

    # Draw contours on image
    image=cv2.drawContours(image,[approx],-1,(255,0,0),-1)
    return path