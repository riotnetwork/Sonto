#!/usr/bin/env python

__author__ = "Jarryd Bekker"
__copyright__ = "Copyright 2014, Bushveld Labs"
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Jarryd Bekker"
__email__ = "jarryd@bushveldlabs.com"
__status__ = "development"


from struct import *
from time import sleep

import serial


class Camera:

    def __init__(self,port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.filename = "image"


    ########################################################################

    def __del__(self):
        print("Closing serial port")
        self.ser.close()
    
    ########################################################################

    def Capture(self, filename):
    
        self.filename = filename
        
        print("* Capturing image:")
        
        if(self.__connect() == "CONNECTED"):
            if(self.__initialize() == "INITIALIZED"):
                if(self.__snapshot() == "CAPTURED"):
                    self.__getpicture()

    ########################################################################

    def __connect(self):
    
        #  Connect to serial port
        
        self.ser = serial.Serial(
            port=self.port, 
            baudrate=self.baudrate, 
            timeout=0.01,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )         
        
        for attempt in range(60):
        
            print("  - Attempt: "+str(attempt)+" at "+str(self.baudrate)+" baud")
            
            # Send sync message
            self.ser.write(self.__msg_sync())
            
            # Read response up to 6 bytes or timeout
            self.response = self.ser.read(6)
            
            # If an ACK is received, wait for a SYNC response
            if (len(self.response) == 6 and self.response[0]=='\xAA'):
            
                # Check that resonse is an ACK to the SYNC command
                if (self.response[1]=='\x0E' and self.response[2]=='\x0D'):
                
                    # Read response up to 6 bytes or timeout
                    self.response = self.ser.read(6)
                    
                    # If a sync response is received, reply with an ACK message
                    if (len(self.response) == 6 and self.response[0]=='\xAA'):
                    
                        # Check that resonse is an SYNC command
                        if (self.response[1]=='\x0D'):
                            
                            # Send sync message
                            self.ser.write(self.__msg_ack(package_id=0))
                        
                            print("  - Connected to camera")
                            return("CONNECTED")
                    
        else:
        
            self.ser.close()
            
            self.ser = serial.Serial(
                port=self.port, 
                baudrate=14400, 
                timeout=0.01,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS
        )   
            
            for attempt in range(60):
            
                print("  - Attempt: "+str(attempt)+" at 14400 baud")
                
                # Send sync message
                self.ser.write(self.__msg_sync())
                
                # Read response up to 6 bytes or timeout
                self.response = self.ser.read(6)
                
                # If an ACK is received, wait for a SYNC response
                if (len(self.response) == 6 and self.response[0]=='\xAA'):
                
                    # Check that resonse is an ACK to the SYNC command
                    if (self.response[1]=='\x0E' and self.response[2]=='\x0D'):
                    
                        # Read response up to 6 bytes or timeout
                        self.response = self.ser.read(6)
                        
                        # If a sync response is received, reply with an ACK message
                        if (len(self.response) == 6 and self.response[0]=='\xAA'):
                        
                            # Check that resonse is an SYNC command
                            if (self.response[1]=='\x0D'):
                                
                                # Send sync message
                                self.ser.write(self.__msg_ack(package_id=0))
                            
                                print("  - Connected to camera")
                                return("CONNECTED")
                       
            else:
                print("No response from camera")
                return("ERROR1")
    
            
    def __initialize(self):
        
        # Send initial message
        self.ser.write(self.__msg_initial(interface_speed=self.baudrate, resolution='VGA'))
        
        # Read response up to 6 bytes or timeout
        self.response = self.ser.read(6)
        
        
        self.ser.close()
        
        
        self.ser = serial.Serial(
            port=self.port, 
            baudrate=self.baudrate, 
            timeout=1,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
            )
        

        
        # If an ACK is received, wait for a SYNC response
        if (len(self.response) == 6 and self.response[0]=='\xAA'):
            
            # Check that resonse is an ACK to the INITIAL command
            
            if (self.response[1]=='\x0E' and self.response[2]=='\x01'):
                
                sleep(0.05)
                
                # Send Set Package Size message
                self.ser.write(self.__msg_setpackagesize())
                
                # Read response up to 6 bytes or timeout
                self.response = self.ser.read(6)
                
                # Check for ACK response
                if (len(self.response) == 6 and self.response[0]=='\xAA'):
                    
                    # Check that resonse is an ACK to the INITIAL command
                    if (self.response[1]=='\x0E' and self.response[2]=='\x06'):
                        print("  - Initialized")
                        return("INITIALIZED")
                    
                else:
                    return("ERROR1")
            else:
                return("ERROR2")
        else:
            return("ERROR3")
        
    def __snapshot(self):
        
        # Send initial message
        self.ser.write(self.__msg_snapshot())
        
        # Read response up to 6 bytes or timeout
        self.response = self.ser.read(6)
        
        # If an ACK is received, wait for a SYNC response
        if (len(self.response) == 6 and self.response[0]=='\xAA'):
            
            # Check that resonse is an ACK to the INITIAL command        
            if (self.response[1]=='\x0E' and self.response[2]=='\x05'):
            
                print("  - Image captured")
                return("CAPTURED")
                
            else:
                return("ERROR1")
                
        else:
            return("ERROR2")
        
    def __getpicture(self):
        
        # Send initial message
        self.ser.write(self.__msg_getpicture())
        
        # Read response up to 6 bytes or timeout
        self.response = self.ser.read(6)
        
        # If an ACK is received,
        if (len(self.response) == 6 and self.response[0]=='\xAA'):
            
            # Check that resonse is an ACK to the GETPICTURE command
            
            if (self.response[1]=='\x0E' and self.response[2]=='\x04'):
                
                # Read response up to 6 bytes or timeout
                self.response = self.ser.read(6)
                
                # If an ACK is received,
                if (len(self.response) == 6 and self.response[0]=='\xAA' and self.response[1]=='\x0A'):
                    # Determine image size
                    self.imgsize = unpack('I',self.response[3]+self.response[4]+self.response[5]+'\x00')
                    
                    # Calculate number of packets to download
                    self.package_count = self.imgsize[0]/(512-6)
                    if self.imgsize[0]%(512-6) >0:
                        self.package_count = self.package_count+1
                    
                    self.wholeimage = ''
                    f = open(self.filename+".jpg", 'w')
                    
                    for package in range(self.package_count):
                        self.ser.write(self.__msg_ack(package_id=package))
                        
                        # Read response up to 6 bytes or timeout
                        self.image = self.ser.read(512)
                        #print(self.image[0]+self.image[1], hex)
                        
                        self.wholeimage = self.wholeimage + self.image[4:-2]
                        
                    self.ser.write(self.__msg_ack(package_id='TERMINATE'))
                    f.write(self.wholeimage)
                    


                
                return("CAPTURED")
            else:
                return("ERROR1")
        else:
            return("ERROR2")
            

    ########################################################################


    def __msg_initial(self,interface_speed, resolution):
            
        self.msg_start = '\xAA'
        self.msg_cmd_id = '\x01'
    
        # p1 - interface speed
        self.interface_speed_dict = {14400: '\x07',
                                28800: '\x06',
                                57600: '\x05',
                                115200: '\x04',
                                230400: '\x03',
                                460800: '\x02'}
        if (interface_speed in self.interface_speed_dict):
            self.p1 = self.interface_speed_dict[interface_speed]
        else:
            raise NameError('Invalid interface speed')
            
        # p2 - given
        self.p2 = '\x07'
            
        # p3 - given
        self.p3 = '\x00'
            
        # p4 - resolution
        self.resolution_dict = {'VGA': '\x07', 'QVGA': '\x05'}
        if (resolution in self.resolution_dict):
            self.p4 = self.resolution_dict[resolution]
        else:
            raise NameError('Invalid resolution')
            
        self.msg = pack('cccccc', self.msg_start, self.msg_cmd_id, self.p1, self.p2, self.p3, self.p4)
        #ser.write(self.msg)      # Send message to serial port
        
        return(self.msg)
            
    #-----------------------------------------------------------------------

    def __msg_getpicture(self):
        
        self.msg_start = '\xAA'
        self.msg_cmd_id = '\x04'
            
        # p1 - fixed
        self.p1 = '\x01'
            
        # p2 - fixed
        self.p2 = '\x00'
            
        # p3 - fixed
        self.p3 = '\x00'
            
        # p4 - fixed
        self.p4 = '\x00'
        
        self.msg = pack('cccccc', self.msg_start, self.msg_cmd_id, self.p1, self.p2, self.p3, self.p4)
        #ser.write(self.msg)      # Send message to serial port
        
        return(self.msg)
   
    #-----------------------------------------------------------------------

    def __msg_snapshot(self):
    
        self.msg_start = '\xAA'
        self.msg_cmd_id = '\x05'
            
        # p1 - fixed
        self.p1 = '\x00'
            
        # p2 - fixed
        self.p2 = '\x00'
            
        # p3 - fixed
        self.p3 = '\x00'
            
        # p4 - fixed
        self.p4 = '\x00'
        
        self.msg = pack('cccccc', self.msg_start, self.msg_cmd_id, self.p1, self.p2, self.p3, self.p4)
        #ser.write(self.msg)      # Send message to serial port
        
        return(self.msg)
    
    #-----------------------------------------------------------------------

    def __msg_setpackagesize(self):
    
        self.msg_start = '\xAA'
        self.msg_cmd_id = '\x06'
            
        # p1 - fixed
        self.p1 = '\x08'
            
        # Use max package size
        
        # p2 - package size low byte
        self.p2 = '\x00'
            
        # p3 - package size high byte
        self.p3 = '\x02'
            
        # p4 - fixed
        self.p4 = '\x00'
        
        self.msg = pack('cccccc', self.msg_start, self.msg_cmd_id, self.p1, self.p2, self.p3, self.p4)
        #ser.write(self.msg)      # Send message to serial port
        
        return(self.msg)

    #-----------------------------------------------------------------------

    def __msg_reset(self,priority):
    
        self.msg_start = '\xAA'
        self.msg_cmd_id = '\x08'
    
        # p1 - fixed
        self.p1 = '\x00'
             
        # p2 - fixed
        self.p2 = '\x00'
            
        # p3 - fixed
        self.p3 = '\x00'
            
        # p4 - resolution
        priority_dict = {'HIGH': '\xFF', 'LOW': '\x00'}
        if (priority in priority_dict):
            p4 = priority_dict[priority]
        else:
            raise NameError('Invalid resolution')
        
        self.msg = pack('cccccc', self.msg_start, self.msg_cmd_id, self.p1, self.p2, self.p3, self.p4)
        
        return(self.msg)
    
    #-----------------------------------------------------------------------


    def __msg_sync(self):
    
        self.msg_start = '\xAA'
        self.msg_cmd_id = '\x0D'
            
        # p1 - fixed
        self.p1 = '\x00'
            
        # p2 - fixed
        self.p2 = '\x00'
            
        # p3 - fixed
        self.p3 = '\x00'
            
        # p4 - fixed
        self.p4 = '\x00'
        
        self.msg = pack('cccccc', self.msg_start, self.msg_cmd_id, self.p1, self.p2, self.p3, self.p4)
        
        return(self.msg)

    #-----------------------------------------------------------------------

    def __msg_ack(self, package_id):
    
        self.msg_start = '\xAA'
        self.msg_cmd_id = '\x0E'
          
        # p1 - fixed
        self.p1 = '\x00'
                
        # p2 - fixed
        self.p2 = '\x00'
            
        if package_id == 'TERMINATE':

            # p3 - fixed
            self.p3 = '\xF0'
                
            # p4 - fixed
            self.p4 = '\xF0'      
        else:
            self.pid = "{0:04d}".format(package_id)
            
            # p3 - fixed
            #self.p3 = pack('c', (self.pid[2]+self.pid[3]).decode("hex"))
            self.p3 = pack('c', chr(int(self.pid[2]+self.pid[3])))
                
            # p4 - fixed
            #self.p4 = pack('c', (self.pid[0]+self.pid[1]).decode("hex"))
            self.p4 = pack('c', chr(int(self.pid[0]+self.pid[1])))
        
        self.msg = pack('cccccc', self.msg_start, self.msg_cmd_id, self.p1, self.p2, self.p3, self.p4)

        
        return(self.msg)
    
    ########################################################################


if __name__ == "__main__":

    myCamera = Camera(port='/dev/ttyS4',baudrate=14400)
    myCamera.Capture()
