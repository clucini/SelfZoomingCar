import numpy as np

# finds the middle of the screen for the central position of the bot

def getOurLocation(helper):
    image = helper['image']
    helper['ourLocation'] = np.array([image.shape[1]/2, image.shape[0]])