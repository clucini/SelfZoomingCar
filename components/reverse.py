def r(helper,memory):
   if memory['reverse']<0:
      memory['reverse']+=1
      return False
   elif memory['reverse']>0:
      memory['angle']=memory['last_angles'][0]
      memory['speed']=1490
      return True
   else:
      return False
   return False;

def beware(helper,memory):
   memory['reverse']-=2
   if memory['reverse']<-20:
        memory['reverse']=20
   r(helper,memory)
