import cv2
import numpy as np
import scipy.signal as signal

def clean(helper):
   #open to remove noise
   bmask=helper['b_mask']
   kernel=np.ones((1,1),np.uint8)
   b_erode = cv2.erode(bmask,kernel)
   # use distance transform
   # Perform the distance transform algorithm
   b_dist = cv2.distanceTransform(b_erode, cv2.DIST_L2, 3)
   #b_dist=np.where(b_dist<3,0,b_dist)
   # find local maxima
   b_max_indx=signal.argrelextrema(b_dist,np.greater_equal,order=1)
   b_maxima=np.zeros(bmask.shape,np.uint8)
   b_maxima[b_max_indx]=1
   b_maxima = cv2.bitwise_and(bmask,bmask,mask=b_maxima)
   cv2.imshow('maxima',b_maxima)