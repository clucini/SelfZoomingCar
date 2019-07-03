import actOnMux as actOn

memory = {}
memory['angle'] = 90
memory['speed'] = 1500
memory['running'] = True

actOnProcess = Thread(target = actOn.move, args=(memory,))

def send_sig(sig):
    if sig == 'a':
        memory['angle'] = 45
    elif sig == 'd':
        memory['angle'] = 135
    elif sig == 'w':
        memory['speed'] = 1565
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

try:
    actOnProcess.start()
except Exception as e:
    print(e)
finally:
    memory['running'] = False
    actOnProcess.join()    
