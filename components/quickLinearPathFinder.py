import cv2
import numpy as np

##TODO:
# Only consider points going in one direction so we don't double up
# Consider all points produced by bitwise_and and sort by distance instead of just taking the first one
# Replace cutting bits off the contour with a contour simplify
# instead of doing normals, doing horizontals seems to be fine as well, (Simulate by setting yellow slicing to 1) maybe include a mode for that if things dont pan out?

# Mode switching from yellow-blue to blue-yellow?

def find_overlaps(y_contours, b_contours):
    #print(type(y_contours))
    #dtype=[('x',int),('y',int)]
    #y_contours=y_contours.astype(dtype)
    #b_contours=b_contours.astype(dtype)
    #y_contours=np.array(y_contours,dtype=dtype)
    #b_contours=np.array(b_contours,dtype=dtype)
    #y_contours.sort(order='y')
    #b_contours.sort(order='y')
    #y_contours=y_contours.astype(int)
    #b_contours=b_contours.astype(int)

    y_contours=y_contours[y_contours[:,1].argsort()]
    b_contours=b_contours[b_contours[:,1].argsort()]

    y_counter = 0
    b_counter = 0

    pairs = []

    for i in range(0, len(y_contours)):
        lastdiff = 100000
        f = 0
        while abs(y_contours[i][1] - b_contours[f][1]) <= lastdiff:
            #print(b_contours[f])
            lastdiff = abs(y_contours[i][1] - b_contours[f][1])
            #print(lastdiff)
            f += 1
            if f >= len(b_contours):
                break
        pairs.append((y_contours[i],b_contours[f-1]))

    return pairs


def getPathToFollow(image):

    # Converts the remaining image from RGB to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Upper and lower bounds for the lines of tape (thanks claudio)
    b_lower = (100, 80, 80)
    b_upper = (110,255,200)

    y_lower = (20, 50, 100)
    y_upper = (35,255,255)

    # Get blue and yellow sections (thanks claudio)
    y_mask = cv2.inRange(hsv, y_lower, y_upper)
    b_mask = cv2.inRange(hsv, b_lower, b_upper)

    # Finds contours in our individual images. This is what we actually use to determine our 2 points of interest.
    # hierarchy isn't in use, but if its not there, the function doesn't work.
    b_contours, hierarchy = cv2.findContours(b_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    y_contours, hierarchy = cv2.findContours(y_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # draw the contours onto the image cos ceebs
    #image=cv2.drawContours(image,b_contours,-1,(0,0,255),-1)
    #image=cv2.drawContours(image,y_contours,-1,(0,255,0),-1)

    # get the largest contours
    main_b_contour = None
    main_b_area = 0
    for i in b_contours:
        area = cv2.contourArea(i)
        #TODO: count contour length instead of area
        
        if area > main_b_area:
            main_b_contour = i
            main_b_area = area

    main_y_contour = None
    main_y_area = 0
    for i in y_contours:
        area = cv2.contourArea(i)
        if area > main_y_area:
            main_y_contour = i
            main_y_area = area

    if main_y_contour is None:
        return None, None, 1
    elif main_b_contour is None:
        return None, 1, None
    main_b_contour=np.reshape(main_b_contour,(main_b_contour.shape[0],main_b_contour.shape[2]))
    main_y_contour=np.reshape(main_y_contour,(main_y_contour.shape[0],main_y_contour.shape[2]))
    #print (main_b_contour)
    pairs=find_overlaps(main_y_contour,main_b_contour)
    parray=np.array(pairs)
    bluepoints=np.reshape(parray[:,1,:],(parray.shape[0],2))
    yellowpoints=np.reshape(parray[:,0,:],(parray.shape[0],2))
    midpoints=(bluepoints+yellowpoints)/2
    return midpoints, yellowpoints, bluepoints

if __name__== '__main__':
    img=cv2.imread("test.png")
    mid,yellow,blue=getPathToFollow(img)
    mid=np.array(mid).astype('int')
    yellow=np.array(yellow).astype('int')
    blue=np.array(blue).astype('int')
    for i,v in enumerate(mid):
        if i<len(mid)-1:
            img=cv2.line(img,tuple(yellow[i]),tuple(blue[i]),(255,0,0))
        img=cv2.circle(img,tuple(v),5,(0,0,255))
    cv2.imshow("result",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    