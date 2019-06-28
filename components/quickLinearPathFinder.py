import cv2
import numpy as np

##TODO:
# Only consider points going in one direction so we don't double up
# Consider all points produced by bitwise_and and sort by distance instead of just taking the first one
# Replace cutting bits off the contour with a contour simplify
# instead of doing normals, doing horizontals seems to be fine as well, (Simulate by setting yellow slicing to 1) maybe include a mode for that if things dont pan out?

# Mode switching from yellow-blue to blue-yellow?

def find_overlaps(y_contours, b_contours):
    y_contours=y_contours[y_contours[:,1].argsort()]
    b_contours=b_contours[b_contours[:,1].argsort()]

    pairs = []
    for i in range(0, len(y_contours)):
        lastdiff = 100000
        f = 0
        if i % np.floor(len(y_contours)/10) != 0:
            continue
        while abs(y_contours[i][1] - b_contours[f][1]) <= lastdiff:
            lastdiff = abs(y_contours[i][1] - b_contours[f][1])
            f += 1
            if f >= len(b_contours):
                break

        pairs.append((y_contours[i],b_contours[f-1]))
    return pairs

def find_lowest(contour):
    cur_r = 0
    cur_e = None

    for e in contour:
        if e[1] > cur_r:
            cur_r = e[1]
            cur_e = e
    return cur_e


def getPathToFollow(helper):
    main_b_contour = helper['main_b_contour']
    main_y_contour = helper['main_y_contour']
    pairs = find_overlaps(main_y_contour,main_b_contour)

    b_lowest = find_lowest(helper['main_b_contour'])
    y_lowest = find_lowest(helper['main_y_contour'])
    if helper['debug']:
        cv2.line(helper['draw_image'], tuple(b_lowest), tuple(y_lowest), (255,255,255), thickness=1)
        cv2.circle(helper['draw_image'], tuple(((b_lowest+y_lowest)/2).astype(int)), 3, (0,0,255), thickness=3)


    parray = np.array(pairs)

    if not parray.size == 0:
        bluepoints=np.reshape(parray[:,1,:],(parray.shape[0],2))
        yellowpoints=np.reshape(parray[:,0,:],(parray.shape[0],2))
        midpoints=(bluepoints+yellowpoints)/2
    else:
        helper['midpoints'] = None
        helper['yellowpoints'] = None
        helper['bluepoints'] = None
        return False

    helper['midpoints'] = midpoints
    helper['yellowpoints'] = yellowpoints
    helper['bluepoints'] = bluepoints
    return True

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
    
