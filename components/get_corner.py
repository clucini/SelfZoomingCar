import cv2

def get_corner(helper):
    for i in range(len(helper['midpoints'])-1):
        cv2.line(helper['draw_image'], tuple(helper['midpoints'][i].astype(int)), tuple(helper['midpoints'][i+1].astype(int)), (255,255,255), 4)

