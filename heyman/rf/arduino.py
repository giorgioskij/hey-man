import serial
from heyman.config import arduino as cfg

port = cfg["port"]

ser = None
try:
    ser = serial.Serial(port)
except:
    print("Could not connect to arduino")


def turnOn():
    if ser != None:
        ser.write(b'1')
        return True
    return False

def turnOff():
    if ser != None:
        ser.write(b'0')
        return True
    return False
