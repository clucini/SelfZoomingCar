import components.seeforward as camera
import components.localiser as localiser
import components.obstacleDetector as obstacleDetector
import components.actOnMux as actOn
import components.followGradient as followLine
import components.getContours as getContours
import components.clean_contours as cc
import components.videowrite as videowriter
import components.fpsCounter as fps
import components.reverse as reverse
import components.steer as steer
import components.calculateAngle as calculateAngle
import components.checkgreen as green
import traceback, cv2, time, math
import numpy as np
from threading import Thread

memory = {}
memory['reverse'] = 0
memory['seen_green'] = False
memory['green_timer'] = False


# FPS stuff
memory['time']=time.time()
memory['minfps']=100
memory['totfps']=0
memory['itercount']=0

# Debug stuff
memory['debug'] = False
memory['record'] = False

# For arduino thread
memory['angle'] = 90
memory['speed'] = 1500
memory['running'] = True

# This is used to actually stop execution of the script. Shouldn't need to be used tbh.
memory['true_stop'] = False


base=1570
boost=60

def reciever(helper):
    # General setup
    global memory
    helper['speed'] = 1560
    helper['angle'] = 90
    helper['debug'] = memory['debug']
    helper['target_point'] = None
    image = helper['image']
    helper['draw_image'] = image.copy()
    localiser.getOurLocation(helper)
    fps.show(memory)

    # Draws a black box over the top of our 'hood'
    height = helper['ourLocation'][1].astype(int)
    width = helper['ourLocation'][0].astype(int)*2

    image[int(height/10*7.5):, int(width/4):int(width/7*6)] = 0
    

    # Get Contours
    getContours.get_c(helper)
    cc.clean(helper)
    
    # Reverse if necessary
    if helper['main_y_contour'] is None and helper['main_b_contour'] is None:
        reverse.beware(helper,memory)
        print('bewareing')
    elif not reverse.r(helper,memory):
        print ('not reversing...')
        if obstacleDetector.amendPath(helper):
            pass
        else:
            steer.s(helper)
        
        if helper['target_point'] is not None:
            calculateAngle.c(helper)
        # Sending stuff to arduino thread
        memory['angle'] = helper['angle']
        memory['speed'] = (1-math.fabs(memory['angle']-90)/45.0)*boost+base
        #memory['speed'] = helper['speed']
    
    # Drawing and recording
    if memory['debug']:
        cv2.imshow("uneditted", image)
        cv2.imshow("drawn", helper['draw_image'])
        cv2.waitKey(1)

    if memory['record']:
        videowriter.writeToFile(helper)

def run():
    global memory
    camera.sendImageTo(reciever)

    actOnProcess = Thread(target = actOn.move, args=(memory,))
    actOnProcess.start()

    try:
        camera.start(memory)
    
    except Exception as e:
        print(e)
        traceback.print_exc()
    finally:
        print('Program stopped succesfully')
        stop_thread(actOnProcess)

def stop_thread(actOnProcess):
    global memory
    memory['running']=False
    actOnProcess.join()


if __name__ == '__main__':
    while not memory['true_stop']:
        input('Press enter when ready: ')
        run()
