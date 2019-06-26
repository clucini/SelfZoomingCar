import cv2
import numpy as np


def get_c(helper):
    image = helper['image']

    blue_im = image.copy()[0:helper['ourLocation'][1].astype(
        int), 0:helper['ourLocation'][0].astype(int)]
    yellow_im = image.copy()
    yellow_im[0:helper['ourLocation'][1].astype(
        int), :helper['ourLocation'][0].astype(int)] = 0

    hsv_yellow = cv2.cvtColor(yellow_im, cv2.COLOR_BGR2HSV)
    hsv_blue = cv2.cvtColor(blue_im, cv2.COLOR_BGR2HSV)
    # Converts the remaining image from RGB to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    helper['hsv'] = hsv  # i need this for later

    # Upper and lower bounds for the lines of tape (thanks claudio)
    b_lower = (100, 60, 100)
    b_upper = (115, 255, 255)

    y_lower = (15, 65, 150)
    y_upper = (30, 255, 255)

    # Get blue and yellow sections (thanks claudio)
    y_mask = cv2.inRange(hsv_yellow, y_lower, y_upper)
    b_mask = cv2.inRange(hsv_blue, b_lower, b_upper)
    helper['b_mask'] = b_mask
    helper['y_mask'] = y_mask
    #cv2.imshow('y_mask', y_mask)
    # cv2.waitKey(1)
    #cv2.imshow('b_mask', b_mask)

    # Finds contours in our individual images. This is what we actually use to determine our 2 points of interest.
    # hierarchy isn't in use, but if its not there, the function doesn't work.
    b_contours, hierarchy = cv2.findContours(
        b_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    y_contours, hierarchy = cv2.findContours(
        y_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    main_b_contour = None
    b_y = -1

    if(b_contours):
        lowest_point = 0
        p = None
        q = -1
        for i in range(len(b_contours)):
            if len(b_contours[i]) < 10:
                continue
            for f in range(len(b_contours[i])):
                if b_contours[i][f][0][1] > lowest_point:
                    lowest_point = b_contours[i][f][0][1]
                    p = i
                    q = f
        if p is not None:
            main_b_contour = b_contours[p]
            if helper['debug']:
                cv2.circle(helper['draw_image'], (b_contours[p][q]
                                                  [0][0], b_contours[p][q][0][1]), 4, (255, 0, 255))
            b_y = b_contours[p][q][0][1]

    main_y_contour = None
    y_y = -1

    if(y_contours):
        lowest_point = 0
        p = -1
        q = -1
        for i in range(len(y_contours)):
            if len(y_contours[i]) < 200:
                continue
            for f in range(len(y_contours[i])):
                if y_contours[i][f][0][1] > lowest_point:
                    lowest_point = y_contours[i][f][0][1]
                    p = i
                    q = f
        if p is not None:
            main_y_contour = y_contours[p]
            #cv2.circle(helper['draw_image'], (y_contours[p][q][0][0], y_contours[p][q][0][1]), 4, (255, 0, 255))
            y_y = y_contours[p][q][0][1]
    if helper['debug']:
        cv2.drawContours(helper['draw_image'],
                         main_y_contour, -1, (0, 255, 0), 3)
        cv2.drawContours(helper['draw_image'],
                         main_b_contour, -1, (0, 255, 0), 3)

    # 50 pixels in 640/480 resolution; more in higher resolution
    minSize = helper['image'].shape[0]*helper['image'].shape[1]*50/648/480
    if main_y_contour is not None:
        if (cv2.contourArea(main_y_contour) < minSize):
            main_y_contour = None
        else:
            main_y_contour = np.reshape(
                main_y_contour, (main_y_contour.shape[0], main_y_contour.shape[2]))
    if main_b_contour is not None:
        if (cv2.contourArea(main_b_contour) < minSize):
            main_b_contour = None
        else:
            main_b_contour = np.reshape(
                main_b_contour, (main_b_contour.shape[0], main_b_contour.shape[2]))

    helper['main_y_contour'] = main_y_contour
    helper['main_b_contour'] = main_b_contour

    # contour gives an array with all the points in the image
    # print('The main yellow: ')
    # print(main_y_contour)
    # print('The main blue: ')
    # print(main_b_contour)
