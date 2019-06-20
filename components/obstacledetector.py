import cv2
import numpy as np
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
    ys=approx[:,:,1].reshape((approx.shape[0]))
    mins=ys.argsort()[-2:]
    minpts=approx[mins,:,:].reshape((2,2))
    print(minpts)
    # Draw a line from edge to edge
    m=(minpts[0,1]-minpts[1,1])/(minpts[0,0]-minpts[1,0])
    b=minpts[0,1]-m*minpts[0,0]
    leftborderpoint=[0,b]
    rightborderpoint=[image.shape[0],m*image.shape[0]+b]
    line=np.zeros(image.shape)
    line=cv2.line(zeros,leftborderpoint,rightborderpoint,255,2)
    # bitwise and it with our yellow and blue contours
    # Upper and lower bounds for the lines of tape (thanks claudio)
    b_lower = (100, 80, 80)
    b_upper = (110,255,200)

    y_lower = (20, 50, 100)
    y_upper = (35,255,255)

    # Get blue and yellow sections (thanks claudio)
    y_mask = cv2.inRange(hsv, y_lower, y_upper)
    b_mask = cv2.inRange(hsv, b_lower, b_upper)

    y_band = np.bitwise_and(y_mask,zeros)
    firstNonzero=np.transpose(np.array(np.nonzero(y_band)))[0]
    cv2.circle(image,tuple(firstNonzero),20,(0,255,255),-1)

    y_band = np.bitwise_and(y_mask,zeros)
    firstNonzero=np.transpose(np.array(np.nonzero(y_band)))[0]
    cv2.circle(image,tuple(firstNonzero),10,255,-1)

    # Draw contours on image
    image=cv2.drawContours(image,[approx],-1,(255,0,0),-1)
    return path