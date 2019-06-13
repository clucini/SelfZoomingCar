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
            targetPoint=np.array(pathToFollow)[0]
            mindist=dist
    print(targetPoint)
    print(ourLocation)
    deviationVector=targetPoint-ourLocation
    deviationVector[1]*=-1
    print(deviationVector)
    print(int(np.arctan2(deviationVector[1], deviationVector[0])*180/np.pi))
    return np.clip(int(np.arctan2(deviationVector[1], deviationVector[0])*180/np.pi),45,135)

if __name__=="__main__":
    print(getCorrection(np.array((320,100)),[np.array((310,80)),np.array((320,90))]))


