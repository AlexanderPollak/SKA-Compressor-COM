import serial,time

class connection:
    def __init__(self):
        ''' Constructor for this class. '''
        self.port = 0


    def open(self, port='/dev/ttyUSB0', baud=19200):
        """ Open serial port for communication
                :param port: path to serial port. Default='/dev/ttyUSB0'
                :param baud: defines the baud rate. Default=19200
                :returns Boolean value True or False """
        self.port = serial.Serial(port,baud, timeout=0.05)
        return self.port.is_open


    def close(self):
        """ Close serial port """
        self.port.close()

    def send_cmd(self,cmd):
        """ Send string via serial connection
                :param cmd: string which gets send via serial link'
                :returns answer from controller in string format """
        self.port.write(cmd)
        time.sleep(0.1)
        return self.port.read(1024)
