import RPi.GPIO as gpio
# import lirc
import time
import asyncio
import atexit
import math

from MotorShield import PiMotor
# from lirc import LircdConnection
import numpy as np

from DistanceSensor import DistanceSensor
from CarPosition import CarPosition
from mapVisualization import SlamPlot
from Gyroskop import Gyroskop

gpio.setmode(gpio.BOARD)

trig = 13
echo = 4
trigBoard = 33
echoBoard = 7
trig = trigBoard
echo = echoBoard

trig2 = 19
echo2 = 20
trigBoard2 = 35
echoBoard2 = 38
trig2 = trigBoard2
echo2 = echoBoard2

distance1 = 10
distance2 = 10

lichtStatus = False
warteZeit = 60 * 15

mFR = PiMotor.Motor("MOTOR3", 1)  # Vorne Rechts
mFL = PiMotor.Motor("MOTOR1", 1)  # Vorne Links

mRR = PiMotor.Motor("MOTOR2", 1)  # Hinten Links
mRL = PiMotor.Motor("MOTOR4", 1)  # Hinten Rechts

#gpio.setup(trig, gpio.OUT)
#gpio.setup(echo, gpio.IN)
#gpio.setup(trig2, gpio.OUT)
#gpio.setup(echo2, gpio.IN)

bootTime = time.time()

print(bootTime)

def increaseSpeed(speed, increase):
    if speed + increase < 100:
        return speed + increase
    else:
        return 100


def decreaseSpeed(speed, increase):
    if speed - increase > -100:
        return speed - increase
    else:
        return -100


def stopMotors():
    mFR.stop()
    mFL.stop()
    mRR.stop()
    mRL.stop()


def changeMotors(front, left, right):
    if front > 0:
        if left == 0 and right == 0:
            mFR.forward(front)
            mFL.forward(front)
            mRR.forward(front)
            mRL.forward(front)
    if front < 0:
        if left == 0 and right == 0:
            mFR.reverse(front * -1)
            mFL.reverse(front * -1)
            mRR.reverse(front * -1)
            mRL.reverse(front * -1)

    if front == 0:
        stopMotors()


def turnStraight():
    mFL.forward(100)
    mFR.forward(100)
    mRL.forward(100)
    mRR.forward(100)


def turnLeft():
    mFL.forward(100)
    mFR.forward(0)
    mRL.forward(100)
    mRR.forward(0)


def turnLeftBack():
    mFL.forward(0)
    mFR.forward(0)
    mRL.forward(0)
    mRR.forward(0)

    mFL.reverse(100)
    mFR.reverse(0)
    mRL.reverse(100)
    mRR.reverse(0)


def turnRightBack():
    mFL.forward(0)
    mFR.forward(0)
    mRL.forward(0)
    mRR.forward(0)

    mFL.reverse(0)
    mFR.reverse(100)
    mRL.reverse(0)
    mRR.reverse(100)


def turnRight():
    mFL.forward(0)
    mFR.forward(100)
    mRL.forward(0)
    mRR.forward(100)


def turnReverse():
    mFL.reverse(100)
    mFR.reverse(100)
    mRL.reverse(100)
    mRR.reverse(100)


def sideStepLeft(timeWait = 0.5):
    stopMotors()
    time.sleep(1)
    turnRightBack()
    time.sleep(timeWait)

    stopMotors()
    time.sleep(1)
    turnLeft()
    time.sleep(timeWait)


def sideStepRight(timeWait = 0.5):
    stopMotors()
    time.sleep(1)
    turnLeftBack()
    time.sleep(timeWait)

    stopMotors()
    time.sleep(1)
    turnRight()
    time.sleep(timeWait)

def exit():
    stopMotors()
    gpio.cleanup()
    print("exit Done")


async def carmain():
    front = 100
    left = 0
    right = 0
    distanceEnable = True

    stopDistanceFront = 15
    stopDistanceLeft = 15

    endCondition = True
    carPos = CarPosition(0, 0, 0)
    obstacles = []  # the map, build from points
    lastStop = 0  # seconds since last time the direction was changed
    sensorDeathLeft = 145
    sensorDeathFront = 145
    sensorFront = DistanceSensor(trig, echo, 3)
    sensorLeft = DistanceSensor(trig2, echo2, 3)
    
    gyroskop = Gyroskop()
   
    vg = 0
    vglast = 0
    vxlast = 0
    vx = 0
    
    vylast = 0
    vy = 0 
    lasttime = time.time()
    currenttime = time.time()
    
    distanceLastFront = 180
    distanceLastLeft = 180
    
    # visual = SlamPlot()
    with open("mapPoints.txt", "w") as f:
        while endCondition:
            
            
            beschleunigungX = gyroskop.getBeschleunigungX(False)
            beschleunigungY = gyroskop.getBeschleunigungY(False)
            
            lastTime = currenttime
            currenttime = time.time()
            print("BeschleunigungX: "+ str(beschleunigungX))
            print("Sekunden"+str(currenttime -lastTime))
            
            vxlast = vx
            vx  = beschleunigungX*(currenttime - lastTime) + vx
            print("Geschwindigkeit X: "+str(vx*3.6)+"Km/h")
            
            vylast = vy
            vy  = beschleunigungY*(currenttime - lastTime) +vy
            print("Geschwindigkeit Y: "+str(vy*3.6)+"Km/h")

                  
            bg = math.sqrt(beschleunigungX**2 + beschleunigungY**2 + 2*beschleunigungX*beschleunigungY)
            vglast = vg
            vg = bg*(currenttime - lastTime)+vglast
            print("Geschwindigkeit Gesamt: "+str(vg*3.6)+"Km/h")
                           
            lastStop = time.time()  # seconds since last time the direction was changed

            if distanceEnable:
                first_awaitable = asyncio.create_task(sensorFront.getDistance())
                second_awaitable = asyncio.create_task(sensorLeft.getDistance())

            if distanceEnable:
                distanceFront = await first_awaitable
                distanceLeft = await second_awaitable
                

            print("=============")
            print("Messung")
            print("Front: ", distanceFront)
            print("Left: ", distanceLeft)
            print("=============")
            
            
            if distanceFront > sensorDeathFront:
                turnReverse()
                
            if distanceLeft > sensorDeathLeft:
                turnRight()
                
            elif distanceEnable and distanceLastFront > distanceFront and distanceFront < stopDistanceFront:  # wall in front of car
                
                if distanceLastLeft <= distanceLeft and distanceLeft < 90 and distanceLeft > stopDistanceLeft:
                    sideStepLeft()
                else:
                    sideStepRight()
                    
                vx = 0
                vy = 0
                vg = 0      
                v = (0, 0, 0)  # TODO the velocity
                carPos.updatePostition(lastStop)
                obstacles.append(carPos.getWallPoint())
                f.write(str(obstacles[-1]) + "\n")
                f.write(str(carPos.x)+"_"+str(carPos.y)+"_"+str(carPos.theta) + "\n")
            elif distanceEnable and distanceLastLeft > distanceLeft and distanceLeft < stopDistanceLeft:  # no wall left of car
                print("Stop Left")

                sideStepRight()

                vx = 0
                vy = 0
                vg = 0
                v = (0, 0, 0)  # TODO the velocity
                carPos.updatePostition(lastStop)
                obstacles.append(carPos.getWallPoint())
                f.write(str(obstacles[-1]) + "\n")
                f.write(str(carPos.x)+"_"+str(carPos.y)+"_"+str(carPos.theta) + "\n")
            
            elif distanceEnable and distanceLastLeft > distanceLeft and distanceLeft < stopDistanceLeft * 2 and distanceFront < stopDistanceFront * 2:
                print("=Stop Front and Left Distance =")

                sideStepRight()
                vx = 0
                vy = 0
                vg = 0
                carPos.updatePostition(lastStop)
                obstacles.append(carPos.getWallPoint())
                f.write(str(obstacles[-1]) + "\n")
                f.write(str(carPos.x)+"_"+str(carPos.y)+"_"+str(carPos.theta) + "\n")
                
            elif distanceLeft > stopDistanceLeft and distanceFront > stopDistanceFront and distanceFront < sensorDeathFront:
                print("=No Obstacles, Forward=")
                turnStraight()

            distanceLastFront = distanceFront
            distanceLastLeft = distanceLeft

# visual.update_plot(obstacles)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # Side note: Apparently, async() will be deprecated in 3.4.4.
    # See: https://docs.python.org/3.4/library/asyncio-task.html#asynio.async
    
    atexit.register(exit)

    try:
        tasks = asyncio.gather(
            asyncio.run(carmain())
        )
        loop.run_until_complete(tasks)
    except KeyboardInterrupt as e:
        print("Caught keyboard interrupt. Canceling tasks...")
    finally:
        exit()
        print("System End. Canceling Task. Stopping Motors. Cleaning GPIO")




