import sys
import glob
import struct
import time
import serial

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/ttyACM*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    print ("Available ports: {0}".format(ports))
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


noPort=False
availablePorts = serial_ports()
if len(availablePorts)==0:
    # be fake
    noPort=True
else:
    port=availablePorts[0]
if not noPort:
    ser = serial.Serial(port, 9600, timeout = None)

time.sleep(1)

def move(memory):
    
    while memory['running']:
        if not noPort:
            ser.write(str(int(memory['angle'])).encode())
            a = ser.readline().decode()
            if a.strip() != str(int(memory['angle'])):
                print('Angle Read Incorrectly:', a.strip())
                print('Angle Read Expected:', memory['angle'])
                print('')
            ser.write(str(int(memory['speed'])).encode())
            a = ser.readline().decode()
            if a.strip() != str(int(memory['speed'])):
                print('Speed Read Incorrectly:', a.strip())
                print('Speed Read Expect:', '1560')
                print('')
        else:
            time.sleep(1)