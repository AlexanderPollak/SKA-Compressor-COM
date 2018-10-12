import serial,time























class com:
    """This class implements the serial connection functions """

    def __init__(self):
        ''' Constructor for this class. '''
        self.port = 0




    def open(self, port='/dev/ttyUSB0', baud=19200):
        """ Open serial port for communication
                :param port: path to serial port. Default='/dev/ttyUSB0'
                :param baud: defines the baud rate. Default=19200
                :returns Boolean value True or False """
        self.port = serial.Serial(port,baud, timeout=0.05)
        self.sensor = sensor(self.port)
        return self.port.is_open


    def close(self):
        """ Close serial port """
        self.port.close()
        del self.sensor

    def send_cmd(self,cmd):
        """ Send string via serial connection
                :param cmd: string which gets send via serial link'
                :returns answer from controller in string format """
        self.port.write(cmd)
        time.sleep(0.1)
        return self.port.read(1024)




class sensor:
    """This class implements sensor readout functions"""

    def __init__(self,port):
        ''' Constructor for this class. '''
        self.port=port


    def enable_averaging(self):
        """ This function enables the sensor averaging
                :returns Boolean True or False for command acknowledged """
        self.port.write('*AE\r')
        time.sleep(0.1)
        rec_str = self.port.read(1024)
        if rec_str=='*S\r':
            return True
        else:
            return False

    def disable_averaging(self):
        """ This function disables the sensor averaging
                :returns Boolean True or False for command acknowledged """
        self.port.write('*AD\r')
        time.sleep(0.1)
        rec_str = self.port.read(1024)
        if rec_str=='*S\r':
            return True
        else:
            return False




    def contr_voltage(self):
        """ Request the sensor value for the controller voltage
                :returns int  """
        self.port.write('*SS,01\r')
        time.sleep(0.1)
        rec_str = self.port.read(1024)
        p=rec_str.find('*S,01:')+len('*S,01:')
        if p==-1:
            return 0
        else:
            return int(rec_str[p:len(rec_str)])

    def contr_current(self):
        """ Request the sensor value for the controller current
                :returns int in mA """
        self.port.write('*SS,02\r')
        time.sleep(0.1)
        rec_str = self.port.read(1024)
        p=rec_str.find('*S,02:')+len('*S,02:')
        if p==-1:
            return 0
        else:
            return int(rec_str[p:len(rec_str)])


    def contr_temperature(self):
        """ Request the sensor value for the controller current
                :returns int in mA """
        self.port.write('*SS,03\r')
        time.sleep(0.1)
        rec_str = self.port.read(1024)
        p=rec_str.find('*S,03:')+len('*S,03:')
        if p==-1:
            return 0
        else:
            return int(rec_str[p:len(rec_str)])
