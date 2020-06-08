import RPi.GPIO as gpio
import time

def init():
    gpio.setmode(gpio.BCM)
    gpio.setup(18,gpio.OUT) #front
    gpio.setup(23,gpio.OUT) # back
    gpio.setup(24,gpio.OUT) # left
    gpio.setup(25,gpio.OUT) # right
    
def end():
    gpio.cleanup()

def move(direction,duration = 10):
    if direction == "front":
        front(duration)
        
    if direction == "back":
        back(duration)
        
    if direction == "right":
        right(duration)
        
    if direction == "left":
        left(duration)
    
def front(duration = 10):
    
    pb = gpio.PWM(23,50)
    pb.start(0)
    pf = gpio.PWM(18,50)
    pf.start(0)

    for x in range(90,100):
        print("for: {}".format(x))
        pf.ChangeDutyCycle(x)
        #pb.ChangeDutyCycle(x)
        time.sleep(duration)
    
    pf.stop()
    pb.stop()
        
def back(duration = 10):
    p = gpio.PWM(23,50)
    p.start(1)
    p.ChangeDutyCycle(30)
    time.sleep(duration)
    p.ChangeDutyCycle(1)
    p.stop()

def left(duration = 10):
    p = gpio.PWM(24,50)
    p.start(1)
    p.ChangeDutyCycle(30)
    time.sleep(duration)
    p.ChangeDutyCycle(1)
    p.stop()
    
def right(duration = 10):
    p = gpio.PWM(25,50)
    p.start(1)
    p.ChangeDutyCycle(30)
    time.sleep(duration)
    p.ChangeDutyCycle(1)
    p.stop()
    
def main():
    init()
    inputDirection = input("front,back,right or left? end to end")
  
    while(inputDirection != "end"):
        try:
            duration = int(input("time ?"))
        except ValueError:
            duration = 10
        else:
            duration = 10
            
        move(inputDirection, duration)
        
        inputDirection = input("front,back,right or left? end to end")
        
    end();

main()