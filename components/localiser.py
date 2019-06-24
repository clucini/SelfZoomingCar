import numpy as np
def getOurLocation(helper):
    image = helper['image']
    helper['ourLocation'] = np.array([image.shape[1]/2, image.shape[0]]) 