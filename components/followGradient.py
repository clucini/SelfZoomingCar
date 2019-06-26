import numpy as np
def follow(helper,blueOrYellow):
    cntr=None
    if blueOrYellow == 'blue': 
        cntr=helper['main_b_contour']
    else:
        cntr=helper['main_y_contour']
    delta = cntr[1:,:]-cntr[:-1,:]
    # eliminate level points
    delta=delta[np.nonzero(delta[:,1])]
    delta=delta[np.nonzero(delta[:,0])]
    
    #print (delta)
    angles=np.arctan2(delta[:,1],delta[:,0])
    meanangle=np.mean(angles)
    # yellow contours are counterclockwise, so correct
    if (meanangle<0):
        meanangle=np.pi/2-meanangle
    # generate a fake point which writes the angle
    helper['midpoints']=[helper['ourLocation']+np.array((100*np.cos(meanangle),-100*np.sin(meanangle)))]