import cv2

def check(helper, memory):
    isThereGreen = False
    
    green_lower = (45, 60, 60)
    green_upper = (55,255,255)
    green_mask = cv2.inRange(hsv, green_lower, green_upper)
    
    cnts = cv2.findContours(green_mask,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)[0]
    c_count = 0
    cur = None
    for e in cnts:
        if len(c_count < len(e)):
            cur = e
            c_count = len(e)

    # if no obstacles, break
    if cur is not None and c_count < 40:
        pass

    if memory['seen_green']:
        # We're currently on the home stretch
        pass

