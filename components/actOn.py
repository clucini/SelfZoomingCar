import serial
import struct
import time
usbport = 'COM4'
ser = serial.Serial(usbport, 9600, timeout = None)

time.sleep(1)

def move(angle):
    ser.write(str(angle).encode())
    a = ser.readline().decode()
    if a.strip() != str(angle):
        print(a)
    ser.write(str("1575").encode())
    a = ser.readline().decode()
    if a.strip() != "1575":
        print(a)

