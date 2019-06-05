import serial
import struct
import time
usbport = 'COM4'
ser = serial.Serial(usbport, 9600, timeout = None)


time.sleep(1)

def move(angle):
    ser.write(str(angle).encode())

# while(1):

#     number += 10
#     if number > 135:
#         number = 45
#     move(number)
#     #time.sleep(0.2)

#     b = '''
#     a = input("Value: ")
#     try:
#         int(a)
#     except:
#         print("Invalid")
#         continue
#     move(a)
#     '''
