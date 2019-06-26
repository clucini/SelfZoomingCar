import numpy as np
def follow(helper,blueOrYellow):
    # shift the line 10px to the left or right depending on whether we are using blue or yellow
    cntr=None
    delta=0
    if blueOrYellow == 'blue': 
        cntr=helper['main_b_contour']
        delta=300
    else:
        cntr=helper['main_y_contour']
        delta=-300
    cntr=cntr.reshape((cntr.shape[0],2))
    cntr[:,0]+=delta
    # clip pixels below a certain height
    helper['midpoints']=cntr[np.where(cntr[:,1]==np.amax(cntr[:,1],0)),:][0]
    print (cntr[np.where(cntr[:,1]==np.amax(cntr[:,1],0)),:].shape)
    #[cntr[np.amax(cntr[:,1].reshape(cntr.shape[0])),:]]
    #cntr=cntr[np.where(cntr[:,1]<380)]
    #cntr=cntr[::30,:]
    #helper['midpoints']=cntr
