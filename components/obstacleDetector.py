import cv2
import numpy as np

# TODO: 
# if the obstacle is outside the track.

# finds the midpoint of the thing
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

def find_rightmost(contour):
    cur_r = 0
    cur_e = None

    for e in contour:
        if e[0] > cur_r:
            cur_r = e[0]
            cur_e = e
    return cur_e

def find_leftmost(contour):
    cur_r = 100000
    cur_e = None

    for e in contour:
        if e[0] < cur_r:
            cur_r = e[0]
            cur_e = e
    return cur_e


# This is some interesting code
# To the best of my understanding, it forms 2 triangles, and if they follow in opposite directions, the lines intersect
# https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
# http://www.bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)


# pushes us to the mdipoint
def amendPath(helper):
    # Converts the remaining image from RGB to HSV
    hsv=helper['hsv']
    # threshold out obstacles
    obj_lower = (150, 60, 60)
    obj_upper = (170,255,255)
    obj_mask = cv2.inRange(hsv, obj_lower, obj_upper)
    #cv2.imshow("purpleboi",obj_mask)
    # Get contours
    cnts=cv2.findContours(obj_mask,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)[0]
    # get contour with largest area
    la=300
    laobj=None
    for i in cnts:
        ca=cv2.contourArea(i)
        if ca>la:
            laobj=i
            la=ca

    
    # if no obstacles, break
    if laobj is None or la<40:
        return False

    laobj=np.reshape(laobj,(laobj.shape[0],laobj.shape[2]))

    if helper['main_b_contour'] is not None:
        b_right = find_rightmost(helper['main_b_contour'])
        b_left = find_leftmost(helper['main_b_contour'])
        o_right = find_rightmost(laobj)
        if helper['debug']:
            cv2.circle(helper['draw_image'], tuple(b_right), 4, (0,125,255), thickness=5)
            cv2.circle(helper['draw_image'], tuple(b_left), 4, (0,125,255), thickness=5)
            cv2.line(helper['draw_image'], tuple(b_left), tuple(b_right), (0,125,255), thickness=3)
            cv2.circle(helper['draw_image'], tuple(o_right), 4, (0,125,255), thickness=5)
            cv2.line(helper['draw_image'], tuple(o_right), tuple(helper['ourLocation']), (0,125,255), thickness=3)

        if(intersect(b_right, b_left, o_right, helper['ourLocation'])):
            print("Obstacle behind blue")
            return False
        

    if helper['main_y_contour'] is not None:
        y_right = find_rightmost(helper['main_y_contour'])
        y_left = find_leftmost(helper['main_y_contour'])
        o_left = find_leftmost(laobj)
        if helper['debug']:
            cv2.circle(helper['draw_image'], tuple(y_right), 4, (255,0,125), thickness=5)
            cv2.circle(helper['draw_image'], tuple(y_left), 4, (255,0,125), thickness=5)
            cv2.line(helper['draw_image'], tuple(y_left), tuple(y_right), (255,0,125), thickness=3)
            cv2.circle(helper['draw_image'], tuple(o_left), 4, (255,0,125), thickness=5)
            cv2.line(helper['draw_image'], tuple(o_left), tuple(helper['ourLocation']), (255,0,125), thickness=3)

        if(intersect(y_right, y_left, o_left, helper['ourLocation'])):
            print("Obstacle behind yellow")
            return False

    # Approximate contour to square
    epsilon = 0.1*cv2.arcLength(laobj,True)
    approx = cv2.approxPolyDP(laobj,epsilon,True)
    if helper['debug']:
        # Draw contours on image
        drawImg=helper['draw_image']
        drawImg=cv2.drawContours(drawImg,[approx],-1,(255,255,0),3)
        drawImg=cv2.drawContours(drawImg,[laobj],-1,(255,0,0),-1)
    # Find the lowest set of points in the approximation
    ys=approx[:,:,1].reshape((approx.shape[0]))
    mins=ys.argsort()[-2:]
    try:
       minpts=approx[mins,:,:].reshape((2,2))
    except Exception:
       return False
    xs=minpts[:,0].reshape((minpts.shape[0]))
    mins=xs.argsort()
    minpts=minpts[mins]
    # Find blue and yellow corresponding points.
    blue_contours=helper['main_b_contour']
    yellow_contours=helper['main_y_contour']
    if blue_contours is None:
        bluepair=[minpts[0],np.array((0,minpts[0][1]))]
    else:
        bluepair=find_overlaps(np.array([minpts[0]]),blue_contours)[0]
    bluedist=np.linalg.norm(bluepair[0]-bluepair[1])
    blueresult=((bluepair[0]+bluepair[1])/2).astype(int)
    if yellow_contours is None:
        yellopair=[minpts[1],np.array((hsv.shape[1],minpts[1][1]))]
    else:
        yellopair=find_overlaps(np.array([minpts[1]]),yellow_contours)[0]
    yellowdist=np.linalg.norm(yellopair[0]-yellopair[1])
    yelloresult=((yellopair[0]+yellopair[1])/2).astype(int)
    # find the distance between blues and yellows and choose one
    if (bluedist == yellowdist ==0):
        return False
    if bluedist<yellowdist:
        result=yelloresult
    else:
        result=blueresult
    helper['target_point'] = [result]
    print('Bluedist: ', bluedist)
    print('Yellowdist: ', yellowdist)
    ## now set the angle

    if helper['debug']:
        cv2.circle(drawImg,tuple(result),20,(0,255,255),-1)
    return True

    deviationVector=result-helper['ourLocation']
    deviationVector[1]*=-1
    angle = int(np.arctan2(deviationVector[1], deviationVector[0])*180/np.pi)
    angle = 90 - ((90 - angle) * 2)
    # if not helper['image'] is None and helper['debug']:
        # helper['draw_image']=cv2.line(helper['draw_image'],tuple(helper['ourLocation'].astype(int)),tuple(targetPoint.astype(int)),(255,255,255),10)
    helper['angle']=np.clip(angle,45,135)
