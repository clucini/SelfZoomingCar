import serial
import struct
import time
usbport = '/dev/ttyACM0'
ser = serial.Serial(usbport, 9600, timeout = None)

time.sleep(1)

def move(angle):
    ser.write(str(angle).encode())
    print(ser.readline())
    ser.write(str("1555").encode())
    print(ser.readline())

