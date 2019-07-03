def r(helper,memory):
   if memory['reverse']<0:
      memory['reverse']+=1
      return False
   elif memory['reverse']>0:
      memory['angle']=90
      memory['speed']=1350
      memory['reverse']-=1
      return True
   else:
      return False
   return False;

def beware(helper,memory):
   memory['reverse']-=2
   if memory['reverse']<-7:
        memory['reverse']=10
   memory['angle']=90
   memory['speed']=1560
