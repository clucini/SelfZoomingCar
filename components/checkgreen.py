import cv2
import time

def check(helper, memory):
    isThereGreen = False
    
    green_lower = (55, 20, 20)
    green_upper = (80,255,255)

    green_hsv = helper['hsv'][int(helper['ourLocation'][1].astype(int)/10*5):,]

    green_mask = cv2.inRange(green_hsv, green_lower, green_upper)
    cv2.imshow('green', green_mask)
    
    cnts = cv2.findContours(green_mask, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)[0]
    c_count = 0
    cur = None
    for e in cnts:
        if c_count < len(e):
            cur = e
            c_count = len(e)
    # if we cansee green
    print(c_count)
    if cur is not None and c_count > 40:
        cv2.drawContours(helper['draw_image'], cur, -1, (255, 255, 0), 3)
        if not memory['seen_green']:
            memory['seen_green'] = True
            memory['green_time'] = time.time()
    else:
        if memory['seen_green'] and time.time() - memory['green_time'] > 2:
            memory['running'] = True




