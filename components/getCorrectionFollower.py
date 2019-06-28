import numpy as np
import cv2

# FUNCTION getCorrection(helper)
# gets the difference between the two edge points and gives us the line in the middle



def getCorrection(helper):
    if helper['midpoints'] is None:
        helper['correction']=90
        return
    bntr=np.array(helper['midpoints'])
    # print (bntr.shape)
    belta = bntr[1:,:]-bntr[:-1,:]
    # eliminate level points
    belta=belta[np.nonzero(belta[:,1])]
    belta=belta[np.nonzero(belta[:,0])]  
    #print (delta)
    bngles=np.arctan2(belta[:,1],belta[:,0])
    beanangle=np.mean(bngles)
    if (beanangle<0):
        beanangle=np.pi/2-beanangle
    helper['correction']=np.clip(beanangle,45,135)

if __name__=="__main__":
    helper = {}
    helper['ourLocation'] = [100,0]
    helper['midpoints'] = [4,2,1,10]
    helper['image'] = 0
    print(getCorrection(np.array((320,100))))


