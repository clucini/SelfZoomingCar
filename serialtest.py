import serial
usbport = 'COM4'
ser = serial.Serial(usbport,9600,timeout = 1)


def move(angle):
    s = b''
    ser.write(angle.encode())
    print(ser.read())

while(1):
    
    a = input("vale")
    move(a)

