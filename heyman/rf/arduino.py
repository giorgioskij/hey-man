import serial

port = '/dev/cu.usbmodem141201'

#ser = serial.Serial(port)

def turnOn():
    # ser.write(b'1')
    print('on')

def turnOff():
    #ser.write(b'0')
    print('off')
