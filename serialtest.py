import serial
usbport = '/dev/ttyAMA0'
ser = serial.Serial(usbport,9600,timeout = 1)


def move(angle):
    ser.write(angle.encode())
    print(ser.readline())

while(1):
    a = input("vale")
    move(a)

