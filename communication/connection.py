import serial,time























class com:
    """This class implements the serial connection functions """

    def __init__(self):
        ''' Constructor for this class. '''
        self.port = 0
        self.comp_time_disabled=0



    def open(self, port='/dev/ttyUSB0', baud=19200):
        """ Open serial port for communication
                :param port: path to serial port. Default='/dev/ttyUSB0'
                :param baud: defines the baud rate. Default=19200
                :returns Boolean value True or False """
        self.port = serial.Serial(port,baud, timeout=0.05)
        self.sensor = sensor(self.port)
        self.compressor = compressor(self.port, self.comp_time_disabled)
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
        p=rec_str.find('*S,01:')+6
        if p==5:
            return 0
        else:
            return int(rec_str[p:len(rec_str)])/100.0

    def contr_current(self):
        """ Request the sensor value for the controller current
                :returns int in mA """
        self.port.write('*SS,02\r')
        time.sleep(0.1)
        rec_str = self.port.read(1024)
        p=rec_str.find('*S,02:')+6
        if p==5:
            return 0
        else:
            return int(rec_str[p:len(rec_str)])/10.0

    def contr_temperature(self):
        """ Request the sensor value for the controller temperature
                :returns int in mA """
        self.port.write('*SS,03\r')
        time.sleep(0.1)
        rec_str = self.port.read(1024)
        p=rec_str.find('*S,03:')+6
        if p==5:
            return 0
        else:
            return int(rec_str[p:len(rec_str)])/10.0


    def compressor_supply_pressure(self):
        """ Request the sensor value for the compressor supply pressure
                :returns int in mA """
        self.port.write('*SS,04\r')
        time.sleep(0.1)
        rec_str = self.port.read(1024)
        p=rec_str.find('*S,04:')+6
        if p==5:
            return 0
        else:
            return int(rec_str[p:len(rec_str)])/10.0

    def compressor_return_pressure(self):
        """ Request the sensor value for the compressor return pressure
                :returns int in mA """
        self.port.write('*SS,05\r')
        time.sleep(0.1)
        rec_str = self.port.read(1024)
        p=rec_str.find('*S,05:')+6
        if p==5:
            return 0
        else:
            return int(rec_str[p:len(rec_str)])/10.0

    def compressor_motor_temperature(self):
        """ Request the sensor value for the motor capsule temperature
                :returns int in mA """
        self.port.write('*SS,06\r')
        time.sleep(0.1)
        rec_str = self.port.read(1024)
        p=rec_str.find('*S,06:')+6
        if p==5:
            return 0
        else:
            return int(rec_str[p:len(rec_str)])/10.0

    def compressor_supply_temperature(self):
        """ Request the sensor value for the helium supply temperature
                :returns int in mA """
        self.port.write('*SS,07\r')
        time.sleep(0.1)
        rec_str = self.port.read(1024)
        p = rec_str.find('*S,07:') + 6
        if p == 5:
            return 0
        else:
            return int(rec_str[p:len(rec_str)])/10.0



class compressor:
    """This class implements sensor readout functions"""

    def __init__(self,port,comp_time_disabled):
        ''' Constructor for this class. '''
        self.port=port
        self.comp_time_disabled=comp_time_disabled


    def reset(self):
        """ This function resets the compressor
                :returns Boolean True or False for command acknowledged """
        self.port.write('*RH\r')
        time.sleep(0.1)
        rec_str = self.port.read(1024)
        if rec_str=='*S\r':
            return True
        else:
            return False

    def disable(self):
        """ This function shuts down the compressor
                :returns Boolean True or False for command acknowledged """
        self.port.write('*DH\r')
        time.sleep(0.1)
        rec_str = self.port.read(1024)
        if rec_str=='*S\r':
            self.comp_time_disabled=time.time()
            return True
        else:
            return False

    def enable(self):
        """ This function starts the compressor, with a time delay between shut off, of 10 min
                :returns Boolean True or False for command acknowledged """
        if self.comp_time_disabled +600 <= time.time(): # 600sec time delay before restart of the compressor
            self.port.write('*DH\r')
            time.sleep(0.1)
            rec_str = self.port.read(1024)
            if rec_str=='*S\r':
                return True
            else:
                return False
        else:
            print "The compressor can be restarted in %.1f minutes." % (float(self.comp_time_disabled +600-time.time())/60.0)
            return False