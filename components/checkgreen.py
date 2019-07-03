import cv2
import time

def check(helper, memory):
    isThereGreen = False
    
    green_lower = (55, 40, 40)
    green_upper = (80,255,255)

    green_hsv = helper['hsv'][int(helper['ourLocation'][1].astype(int)/10*4):,]

    green_mask = cv2.inRange(green_hsv, green_lower, green_upper)
    if memory['debug']:
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
    else:
        if memory['seen_green'] and memory['green_timer'] == 0:
            memory['green_timer'] = time.time()
        
        elif memory['seen_green'] and time.time() - memory['green_timer'] > 1:
            memory['running'] = False




