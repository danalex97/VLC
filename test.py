import serial
import time
import sys

class Device():
    def __init__(self):
        self.s = serial.Serial('/dev/ttyACM0',115200, timeout = 1)
        time.sleep(2)

    def send(self, message):
        self.s.write(str.encode(message + "\n"))

    def listen(self):
        bts = self.s.read(10)
        print(str(bts))

if __name__ == "__main__":
    d = Device()
    s = d.s
    # d.send("p")
    # d.read()

    # s.write(b"r\n")
    # time.sleep(0.1)

    # #write to the device’s serial port
    s.write(b"a[AB]\n") #set the device address to AB
    time.sleep(0.1) #wait for settings to be applied
    s.write(b"c[1,0,5]\n") #set number of retransmissions to 5
    time.sleep(0.1) #wait for settings to be applied
    s.write(b"c[0,1,30]\n") #set FEC threshold to 30 (apply FEC to packets with payload >= 30)
    time.sleep(0.1) #wait for settings to be applied
    s.write(b"m[hello world!\0,CD]\n") #send message to device with address CD
    #
    # #read from the device’s serial port (should be done in a separate thread)
    message = ""
    while True: #while not terminated
     try:
       byte = s.read(1) #read one byte (blocks until data available or timeout reached)
       byte = byte.decode('UTF-8')

       if byte=='\n': #if termination character reached
         print(message) #print message
         message = "" #reset message
       else:
         # print(byte)
         message = message + byte #concatenate the message
     except serial.SerialException:
       continue #on timeout try to read again
     except KeyboardInterrupt:
       sys.exit() #on ctrl-c terminate program
