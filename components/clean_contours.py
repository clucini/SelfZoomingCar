import cv2
import numpy as np

def clean(helper):
    main_b_contour = helper['main_b_contour']
    main_y_contour = helper['main_y_contour']
    last = 0

    #     print(main_b_contour)
    #     for e in main_b_contour:
    #         if e[1] > last:
    #             last = e[1]
    #             e[1] = 0
    #         else:
    #             last = e[1]
    #     # main_b_contour = np.where(main_b_contour[:, 1] > -1)


    if main_b_contour is not None:
        main_b_contour = main_b_contour[int(len(main_b_contour)/2):]

        for e in main_b_contour:
            cv2.circle(helper['draw_image'], (e[0], e[1]), 4, (0, 0, 255))
            
    if main_y_contour is not None:
        main_y_contour = main_y_contour[int(len(main_y_contour)/2):]

        for e in main_y_contour:
            cv2.circle(helper['draw_image'], (e[0], e[1]), 4, (0, 0, 255))
