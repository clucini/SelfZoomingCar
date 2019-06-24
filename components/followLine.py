def follow(helper,blueOrYellow):
    # shift the line 10px to the left or right depending on whether we are using blue or yellow
    cntr=None
    delta=0
    if blueOrYellow == 'blue': 
        cntr=helper['main_b_contour']
        delta=10
    else:
        cntr=helper['main_y_contour']
        delta=-10
    cntr=cntr.reshape((cntr.shape[0],2))
    # clip pixels below a certain height
