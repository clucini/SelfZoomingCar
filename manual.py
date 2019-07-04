import components.actOnMux as actOn
from threading import Thread
import time
memory = {}
memory['angle'] = 90
memory['speed'] = 1500
memory['running'] = True

actOnProcess = Thread(target = actOn.move, args=(memory,))

def send_sig(sig):
    global memory
    if sig == 'a':
        memory['angle'] = 45
    elif sig == 'd':
        memory['angle'] = 135
    elif sig == 'w':
        memory['speed'] = 1575
    elif sig == 's':
        memory['speed'] = 1440
    elif sig == 'q':
        memory['speed'] = 1500
    else:
        print('No invalid signals')

def listen():
    while True:
        a = input("Signal: ")
        send_sig(a[0])

actOnProcess.start()
send_sig('w')
for i in range(0,10):
    send_sig('a')
    time.sleep(0.25)
    send_sig('d')
    time.sleep(0.25)

time.sleep(0.5)
send_sig('q')

try:
    listen()
except Exception as e:
    print(e)
finally:
    memory['running'] = False
    actOnProcess.join()    

listen()
