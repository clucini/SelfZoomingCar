import components.seeforward as camera
import components.localiser as localiser
import components.obstacleDetector as obstacleDetector
import components.actOnMux as actOn
import components.followGradient as followLine
import components.getContours as getContours
import components.clean_contours as cc
import components.videowrite as videowriter
import components.fpsCounter as fps
import components.steer as steer
import calculateAngle as calculateAngle
import traceback, cv2, time
import numpy as np
from threading import Thread

memory = {}
memory['reverse'] = 0

# FPS stuff
memory['time']=time.time()
memory['minfps']=100
memory['totfps']=0
memory['itercount']=0

# Debug stuff
memory['debug'] = True
memory['record'] = False

# For arduino thread
memory['angle'] = 90
memory['speed'] = 1575
memory['running'] = True

def reciever(helper):
    # General setup
    global memory
    helper['speed'] = 1575
    helper['correction'] = 90
    helper['debug'] = memory['debug']
    helper['target_point']
    image = helper['image']
    helper['draw_image'] = image.copy()
    localiser.getOurLocation(helper)
    fps.show(memory)

    # Draws a black box over the top of our 'hood'
    height = helper['ourLocation'][1].astype(int)
    width = helper['ourLocation'][0].astype(int)*2

    image[int(height/10*7.5):, int(width/4):int(width/6*5)] = 0
    

    # Get Contours
    getContours.get_c(helper)
    cc.clean(helper)
    
    
    if helper['main_y_contour'] is None and helper['main_b_contour'] is None:
        helper['speed'] = 1500
    elif helper['main_y_contour'] is None:
        followLine.follow(helper,'blue')    
    elif helper['main_b_contour'] is None:
        followLine.follow(helper,'notbluethiscanbeanythingwhyusebooleanssteeven')
    else:
        steer.s(helper)
    
    if helper['target_point']:
        calculateAngle.c(helper)
        
    
    # Sending stuff to arduino thread
    memory['angle'] = helper['angle']
    memory['speed'] = helper['speed']
    
    # Drawing and recording
    if memory['debug']:
        cv2.imshow("uneditted", image)
        cv2.imshow("drawn", helper['draw_image'])
        cv2.waitKey(1)

    if memory['record']:
        videowriter.writeToFile(helper)



if __name__ == '__main__':
    camera.sendImageTo(reciever)
    actOnProcess = Thread(target = actOn.move, args=(memory,))
    actOnProcess.start()

    try:
        camera.start()
    except Exception as e:
        print(e)
        traceback.print_exc()

    finally:
        print('asakjshdakjshdkjahdskjahdshasdfahjafs')
        memory['running']=False
        actOnProcess.join()