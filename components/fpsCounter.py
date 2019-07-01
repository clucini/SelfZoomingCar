import time

def show(memory):
    fps=1/(time.time()-memory['time'])
    # print ("FPS:{0}".format(fps))
    if fps<memory['minfps']:
        memory['minfps']=fps
    # print ("minFPS:{0}".format(memory['minfps']))
    memory['itercount']+=1
    memory['totfps']+=fps
    print("avgfps:{0}".format(memory['totfps']/memory['itercount']))
    memory['time']=time.time()