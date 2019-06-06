#Final code for controlling equipment and cutter through a mobile app
#Part of major project final review


#importing the required packages
import sys
import time
import RPi.GPIO as GPIO

from http.server import BaseHTTPRequestHandler, HTTPServer

#assigning pin number for raspberry pi
myRequest=None
GPIO.setwarnings(False)
GPIO.cleanup()
mode=GPIO.getmode()
Move1=20	#motor 1 (equipment left)
Stop1=26
Pwm1=12
Move2=13	#motor 2 (equipment right)
Stop2=6
Pwm2=19
Move3=5		#motor 3 (cutter left)
Stop3=21
Pwm3=16
Move4=23	#motor 4 (cutter right)
Stop4=25
Pwm4=24


#setting up the pin number on raspberry pi
GPIO.setmode(GPIO.BCM)
GPIO.setup(Move1, GPIO.OUT)
GPIO.setup(Stop1, GPIO.OUT)
GPIO.setup(Pwm1, GPIO.OUT)
GPIO.output(Stop1, GPIO.HIGH)
GPIO.output(Pwm1, GPIO.HIGH)
GPIO.setup(Move2, GPIO.OUT)
GPIO.setup(Stop2, GPIO.OUT)
GPIO.setup(Pwm2, GPIO.OUT)
GPIO.output(Stop2, GPIO.HIGH)
GPIO.output(Pwm2, GPIO.HIGH)
GPIO.setup(Move3, GPIO.OUT)
GPIO.setup(Stop3, GPIO.OUT)
GPIO.setup(Pwm3, GPIO.OUT)
GPIO.output(Stop3, GPIO.HIGH)
GPIO.output(Pwm3, GPIO.HIGH)
GPIO.setup(Move4, GPIO.OUT)
GPIO.setup(Stop4, GPIO.OUT)
GPIO.setup(Pwm4, GPIO.OUT)
GPIO.output(Stop4, GPIO.HIGH)
GPIO.output(Pwm4, GPIO.HIGH)

#function to move forward
def forward():
    GPIO.output(Stop1, GPIO.LOW)
    GPIO.output(Move1, GPIO.HIGH)
    GPIO.output(Stop2, GPIO.LOW)
    GPIO.output(Move2, GPIO.LOW)
    print("Moving Forward")

#function to move backward
def reverse():
    GPIO.output(Stop1, GPIO.LOW)
    GPIO.output(Move1, GPIO.LOW)
    GPIO.output(Stop2, GPIO.LOW)
    GPIO.output(Move2, GPIO.HIGH)
    print("Moving Reverse")

#function to turn left
def left():
    GPIO.output(Stop1, GPIO.LOW)
    GPIO.output(Move1, GPIO.LOW)
    GPIO.output(Stop2, GPIO.LOW)
    GPIO.output(Move2, GPIO.LOW)
    print("Turning Left")

#function to turn right
def right():
    GPIO.output(Stop1, GPIO.LOW)
    GPIO.output(Move1, GPIO.HIGH)
    GPIO.output(Stop2, GPIO.LOW)
    GPIO.output(Move2, GPIO.HIGH)
    print("Turning Right")

#function for the cutter to rotate clockwise
def cutterc():
    GPIO.output(Stop3, GPIO.LOW)
    GPIO.output(Move3, GPIO.HIGH)
    GPIO.output(Stop4, GPIO.LOW)
    GPIO.output(Move4, GPIO.LOW)
    print("Cutter Clockwise")
    #time.sleep(x)
    #GPIO.output(Stop, GPIO.HIGH)

#function for the cutter to rotate anti-clockwise
def cutterac():
    GPIO.output(Stop3, GPIO.LOW)
    GPIO.output(Move3, GPIO.LOW)
    GPIO.output(Stop4, GPIO.LOW)
    GPIO.output(Move4, GPIO.HIGH)
    print("Cutter Anti-clockwise")
    #time.sleep(x)
    #GPIO.output(Stop, GPIO.HIGH)

#funtion to stop the movement of equipment
def stop():
    GPIO.output(Stop1, GPIO.HIGH)
    GPIO.output(Stop2, GPIO.HIGH)


#funtion to stop the cutter rotation
def stopc():
    GPIO.output(Stop3, GPIO.HIGH)
    GPIO.output(Stop4, GPIO.HIGH)

#for receiving and handling the input from the app
class RequestHandler_httpd(BaseHTTPRequestHandler):
    def do_GET(self):
        global myRequest
        myRequest = self.requestline
        myRequest = myRequest[5 : int(len(myRequest) - 9)]
        print('Received:')
        if(myRequest=="F"):
            forward()
        elif(myRequest=="D"):
            reverse()
        elif(myRequest=="R"):
            right()
        elif(myRequest=="L"):
            left()
        elif(myRequest=="CL"):
            cutterc()
        elif(myRequest=="CR"):
            cutterac()
        elif(myRequest=="S"):
            stop()
        elif(myRequest=="OF"):
            stopc()
        print(myRequest)
        messagetosend=bytes(' ',"utf");
        self.send_response(200);
        self.send_header('Content-Type','text/plain')
        self.send_header('Content-Length',len(messagetosend))
        self.end_headers()
        self.wfile.write(messagetosend)
        return

#set the ip address and port number of the pi as the server for sending request
server_address_httpd = ('192.168.43.17',8080)

#starting the server on pi
httpd = HTTPServer(server_address_httpd, RequestHandler_httpd)
httpd.serve_forever()
