import serial
import struct
import time
usbport = 'COM4'
ser = serial.Serial(usbport, 9600, timeout = None)

time.sleep(1)

def move(angle):
    ser.write(str(angle).encode())
    print(ser.readline())
    #ser.write(str("1565").encode())
    #print(ser.readline())
