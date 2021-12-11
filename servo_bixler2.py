import RPi.GPIO as GPIO
import time

#
GPIO.setmode(GPIO.BOARD)

# setting up
GPIO.setup(11,GPIO.OUT)
servo1 = GPIO.PWM(11,50) #live4ground6 aileron
GPIO.setup(12,GPIO.OUT)
servo2 = GPIO.PWM(12,50) #l2g9 aileron
GPIO.setup(13,GPIO.OUT)
servo3 = GPIO.PWM(13,50) #elovater
GPIO.setup(15,GPIO.OUT)
servo4 = GPIO.PWM(15,50) #rudder
servo1.start(0)
servo2.start(0)
servo3.start(0)
servo4.start(0)
#Test Code
def test():
    servo1.start(0)
    time.sleep(2)
    servo1.ChangeDutyCycle(2)
    time.sleep(2)
    servo1.ChangeDutyCycle(7)
    time.sleep(2)
    servo1.ChangeDutyCycle(12)
    time.sleep(2)
    servo1.ChangeDutyCycle(7)

#Functions
def aileron(x):#-2 = left, 2 = right
    print('begin')
    servo1.ChangeDutyCycle(7-x) #right between 9 down and up 5
    servo2.ChangeDutyCycle(7-x) #left between down 5 and up 9
    #time.sleep(2)
    print('end')
    
def elovater(y):
    servo3.ChangeDutyCycle(7-y)
    
def rudder(z):
    print('beg')
    servo4.ChangeDutyCycle(7-z)
    print('d')

def Stop():
    servo1.stop()
    servo2.stop()
    servo3.stop()
    servo4.stop()
    GPIO.cleanup()
    print('Goodbye2')
    
'''def roll(AIx,GYROx): 
    wanted_roll = 0#AI
    actual_roll = 0#GYRO
    x = 0
    while actual_roll != wanted_roll:
        if actual_roll > wanted_roll:
            x-=0.1
        if actual_roll < wanted_roll:
            x+=0.1
        aileron(x)

def pitch(AIy,GYROy):
    wanted_pitch = 0#AI
    actual_pitch = 0#GYRO
    y = 
    if actual_pitch < wanted_pitch:
        elovater +
    if actual_pitch > wanted_pitch:
        elovater -

def yaw(AIz,GYROz):
    wanted_yaw = #AI
    actual_yaw = #GYRO
    z = 0
    if actual_yaw > wanted_yaw: #if glider isn't yawed to the right enough
        Rudder -
    if actual_yaw < wanted_yaw: #if glider isn't yawed to the right enough
        Rudder +'''

    
    
#Real Code
    
    
v = 0
aileron(v)
elovater(v)
rudder(v)
'''aileron(0)
time.sleep(2)
aileron(1)
time.sleep(2)
aileron(2)
time.sleep(2)
aileron(1)
time.sleep(2)
aileron(0)
time.sleep(2)
aileron(-1)
time.sleep(2)
aileron(-2)
time.sleep(2)
aileron(-1)
time.sleep(2)
aileron(0)


#servo1.ChangeDutyCycle(5)
#time.sleep(2)
#clean
servo1.stop()
servo2.stop()
servo3.stop()
servo4.stop()
GPIO.cleanup()
print('Goodbye2')'''