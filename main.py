import RPi.GPIO as gpio
# import lirc
import time
import asyncio
from MotorShield import PiMotor
# from lirc import LircdConnection
import numpy as np
from multiprocessing import Process

from DistanceSensor import DistanceSensor
from CarPosition import CarPosition
from mapVisualization import SlamPlot

gpio.setmode(gpio.BOARD)

trig = 3
echo = 4
trigBoard = 5
echoBoard = 7
trig = trigBoard
echo = echoBoard

trig2 = 2
echo2 = 20
trigBoard2 = 3
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
    print("straight")
    mFL.forward(100)
    mFR.forward(100)
    mRL.forward(100)
    mRR.forward(100)


def turnLeft():
    print("left")
    mFL.forward(100)
    mFR.forward(0)
    mRL.forward(100)
    mRR.forward(0)


def turnLeftBack():
    print("left")
    mFL.forward(0)
    mFR.forward(0)
    mRL.forward(0)
    mRR.forward(0)

    mFL.reverse(100)
    mFR.reverse(0)
    mRL.reverse(100)
    mRR.reverse(0)


def turnRightBack():
    print("right")
    mFL.forward(0)
    mFR.forward(0)
    mRL.forward(0)
    mRR.forward(0)

    mFL.reverse(0)
    mFR.reverse(100)
    mRL.reverse(0)
    mRR.reverse(100)


def turnRight():
    print("right")
    mFL.forward(0)
    mFR.forward(100)
    mRL.forward(0)
    mRR.forward(100)


def turnReverse():
    print("reverse")
    mFL.reverse(100)
    mFR.reverse(100)
    mRL.reverse(100)
    mRR.reverse(100)


def sideStepLeft(timeWait):
    stopMotors()
    time.sleep(1)
    print("Stop Front")
    turnRightBack()
    time.sleep(timeWait)

    stopMotors()
    time.sleep(1)
    turnLeft()
    time.sleep(timeWait)


def sideStepRight(timeWait):
    stopMotors()
    time.sleep(1)
    print("Stop Front")
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

    stopDistanceFront = 10
    stopDistanceLeft = 10 
    endCondition = True 
    carPos = CarPosition(0,0,0)
    obstacles = [] # the map, build from points
    lastStop = time.time() # seconds since last time the direction was changed
    sensorFront = DistanceSensor(trig, echo, 3)
    sensorLeft = DistanceSensor(trig2, echo2, 3)
    p1 = Process(target=sensorFront.run())
    p2 = Process(target=sensorLeft.run())

    p1.run()
    p2.run()
        
   # visual = SlamPlot()
    with open("mapPoints.txt", "w") as f:
        while endCondition:
            distanceFront = sensorFront.lastDistance
            distanceLeft = sensorLeft.lastDistance

            print("=============")
            print("Messung")
            print("Front: ", distanceFront)
            print("Left: ", distanceLeft)
            print("=============")

            if distanceFront < stopDistanceFront:  # wall in front of car
                print("Strop Right")

                carPos.updatePosition(time.time() - lastStop, 0.5*np.pi)
                sideStepRight(1)
                obstacles.append(carPos.getWallPoint())
                f.write(str(obstacles[-1]) + "\n")
                f.write(str(carPos.getPosition()) + "\n\n")
                lastStop = time.time()

            elif distanceLeft < stopDistanceLeft:  # no wall left of car
                print("Stop Left")

                carPos.updatePosition(time.time() - lastStop, 0.5*np.pi)
                sideStepRight(1)
                obstacles.append(carPos.getWallPoint())
                f.write(str(obstacles[-1]) + "\n")
                f.write(str(carPos.getPosition()) + "\n\n")
                lastStop = time.time()

            if distanceLeft > stopDistanceLeft and distanceFront > stopDistanceFront:
                #print("Start")
                turnStraight()


# visual.update_plot(obstacles)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # Side note: Apparently, async() will be deprecated in 3.4.4.
    # See: https://docs.python.org/3.4/library/asyncio-task.html#asynio.async

    try:
        tasks = asyncio.gather(
            asyncio.run(carmain())
        )
        loop.run_until_complete(tasks)
    except KeyboardInterrupt as e:
        exit()

        print("Caught keyboard interrupt. Canceling tasks...")
        tasks.cancel()
        loop.run_forever()
        tasks.exception()
        gpio.cleanup()
    finally:
        exit()
        loop.close()
        gpio.cleanup()


