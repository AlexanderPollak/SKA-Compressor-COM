class connection:
    def __init__(self):
        ''' Constructor for this class. '''
        import serial, time
        self.status = True


    def open(self, port='/dev/ttyUSB0', baud=19200):
        self = serial.Serial(port,baud, timeout=0.05)
        return self

    def close(self):
        self.close()

    def send_cmd(self,cmd):
        self.write(cmd)
        time.sleep(0.1)
        return self.read(1024)
