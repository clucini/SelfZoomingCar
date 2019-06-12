import serial
import struct
import time
usbport = '/dev/ttyACM0'
ser = serial.Serial(usbport, 9600, timeout = None)


time.sleep(1)

def move(angle):
    ser.write(str(angle).encode())
    print(ser.readline())

# while(1):

#     a = input("Value: ")
#     try:
#         int(a)
#     except:
#         print("Invalid")
#         continue
#     move(a)
