import cv2
import numpy as np


def get_c(helper):
    image = helper['image']
    # Converts the remaining image from RGB to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Upper and lower bounds for the lines of tape (thanks claudio)
    b_lower = (100, 100, 100)
    b_upper = (115, 255, 255)

    y_lower = (15, 150, 150)
    y_upper = (30, 255, 255)

    # Get blue and yellow sections (thanks claudio)
    y_mask = cv2.inRange(hsv, y_lower, y_upper)
    b_mask = cv2.inRange(hsv, b_lower, b_upper)

    # Finds contours in our individual images. This is what we actually use to determine our 2 points of interest.
    # hierarchy isn't in use, but if its not there, the function doesn't work.
    b_contours, hierarchy = cv2.findContours(b_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    y_contours, hierarchy = cv2.findContours(y_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    main_b_contour = None
    b_y = -1

    if(b_contours):
        lowest_point = 0
        p = -1
        q = -1
        for i in range(len(b_contours)):
            if len(b_contours[i]) < 20:
                continue
            for f in range(len(b_contours[i])):
                if b_contours[i][f][0][1] > lowest_point:
                    lowest_point = b_contours[i][f][0][1]
                    p = i
                    q = f
        
        main_b_contour = b_contours[p]

        b_y = b_contours[p][q][0][1]

    main_y_contour = None
    y_y = -1
        
    if(y_contours):
        lowest_point = 0
        p = -1
        q = -1
        for i in range(len(y_contours)):
            if len(y_contours[i]) < 20:
                continue
            for f in range(len(y_contours[i])):
                if y_contours[i][f][0][1] > lowest_point:
                    lowest_point = y_contours[i][f][0][1]
                    p = i
                    q = f

        main_y_contour = y_contours[p]

        # cv2.circle(c2, (y_contours[p][q][0][0], y_contours[p][q][0][1]), 4, (255, 0, 255))
        y_y = y_contours[p][q][0][1]


    helper['main_y_contour'] = main_y_contour
    helper['main_b_contour'] = main_b_contour

    if main_y_contour is None or main_b_contour is None:
        return None

    cv2.drawContours(image, main_y_contour, -1, (0,255,0), 3)
    cv2.drawContours(image, main_b_contour, -1, (0,255,0), 3)

    main_b_contour=np.reshape(main_b_contour,(main_b_contour.shape[0],main_b_contour.shape[2]))
    main_y_contour=np.reshape(main_y_contour,(main_y_contour.shape[0],main_y_contour.shape[2]))

    helper['main_y_contour'] = main_y_contour
    helper['main_b_contour'] = main_b_contour


