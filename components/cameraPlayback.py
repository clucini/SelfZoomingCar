import numpy as np
import cv2


func_to_send_to = None

def sendImageTo(func):
    global func_to_send_to
    func_to_send_to = func
def start():
    cap = cv2.VideoCapture('vids/sanename.avi')

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # send
        func_to_send_to(frame)
        cv2.waitKey(0)

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
