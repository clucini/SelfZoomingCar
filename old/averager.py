prev = 0
factor=0.1
def adjust(helper,varname):
    global prev
    number=helper[varname]
    if (prev==0):
        prev=number 
    prev=(number*(1-factor)+prev*factor)
    helper[varname]=prev