import cv2
import numpy as np

##TODO:
# Only consider points going in one direction so we don't double up
# Consider all points produced by bitwise_and and sort by distance instead of just taking the first one
# Replace cutting bits off the contour with a contour simplify
# instead of doing normals, doing horizontals seems to be fine as well, (Simulate by setting yellow slicing to 1) maybe include a mode for that if things dont pan out?

# Mode switching from yellow-blue to blue-yellow?

def getX(dx,dy,x,y,y1):
    if dy==0:
        return -1
    return x-(dx*(y-y1)/dy)

def getY(dx,dy,x,y,x1):
    if dx==0:
        return -1
    return y-(dy*(x-x1)/dx)

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
    
    # get the largest contours
    main_b_contour = None
    main_b_area = 0
    for i in b_contours:
        area = cv2.contourArea(i)
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
        
    # take only one in every 5 points from the contour
    #print(main_b_contour)
    #main_b_contour = main_b_contour[::2]
    main_y_contour = main_y_contour[::1]
    #pgrint(main_b_contour)
    # for just the yellow contour, draw normals which meet the blue contour
    # to do this, since i cbs to do a bunch of linear algebra, we'll draw the blue contour and then draw lines and then do a bitmask
    # first draw the blue contour and cache it
    blue_contour=np.zeros(image.shape[0:2]).astype('uint8')
    cv2.drawContours(blue_contour,[main_b_contour],0,1,-1)

    #yellow_contour=np.zeros(image.shape[0:2]).astype('uint8')
    #cv2.drawContours(yellow_contour,main_y_contour,0,1,-1)
    #cv2.imshow("result",blue_contour*255)
    #cv2.waitKey(0)
    
    # some debugging relics
    drep=np.copy(image)

    blue_contour=blue_contour.astype('bool')
    midpoints = []
    yellowpoints = []
    bluepoints = [] 
    for i, v in enumerate(main_y_contour):
        if (i == len(main_y_contour)-1):
            # prevent crashing on final point
            break
        nextPoint = main_y_contour[i+1]
        if (v[0][1]>nextPoint[0][1]):
            continue
        midpoint = ((v + nextPoint)/2)[0]
        lineStart=(0,int(midpoint[1]))
        lineEnd=(image.shape[1],int(midpoint[1]))
        linemask=np.zeros(image.shape[0:2])
        #print (successfulcoords)
        linemask=cv2.line(linemask,lineStart,lineEnd,1,2).astype('bool')
        # cv2.imshow("result",linemask.astype('uint8')*255)
        #cv2.waitKey(0)
        bitand=linemask*blue_contour

        _bitand=np.copy(bitand).astype('uint8')*255
        _bitand=cv2.erode(_bitand,(5,5))
        #cv2.imshow("result",_bitand)
        #cv2.waitKey(1)
        if (np.sum(bitand)>0):
            # Find first nonzero cooordinate
            # print("Sum: ", np.sum(bitand))
            firstNonzero=np.transpose(np.array(np.nonzero(bitand)))[0]
            t=firstNonzero[0]
            firstNonzero[0]=firstNonzero[1]
            firstNonzero[1]=t
            cv2.circle(_bitand,tuple(firstNonzero),10,255,-1)
            # cv2.imshow("result",_bitand)
            # cv2.waitKey(1)
            # Calculate the midpoint
            midmidpoint=(firstNonzero+midpoint)/2
            midpoints.append(midmidpoint)
            yellowpoints.append(midpoint)
            bluepoints.append(firstNonzero)
            # Add midpoint to return list
  
    return midpoints, yellowpoints, bluepoints

if __name__== '__main__':
    img=cv2.imread("test.png")
    print(img.shape)
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
    