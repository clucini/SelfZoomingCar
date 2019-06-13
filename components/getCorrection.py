import numpy as np
def getCorrection(ourLocation,pathToFollow):
    # Trim based on path
    radius=5
    minDist=10000
    #just to initialise
    targetPoint=ourLocation
    centre=np.array((0,1))
    for i in pathToFollow:
        dist=np.linalg.norm(i-ourLocation)
        if dist>radius and dist<minDist:
            targetPoint=pathToFollow
            mindist=dist
    deviationVector=targetPoint-ourLocation
    return np.arccos(np.dot(deviationVector,centre)/np.linalg.norm(deviationVector)*np.linalg.norm(centre))*180/np.pi()