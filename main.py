import RPi.GPIO as gpio
import lirc
import time
import asyncio
from MotorShield import PiMotor
from lirc import LircdConnection
import numpy as np

from DistanceSensor import DistanceSensor
from CarPosition import CarPosition
from mapVisualization import SlamPlot

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

m1 = PiMotor.Motor("MOTOR2", 1)
m2 = PiMotor.Motor("MOTOR3", 1)

m3 = PiMotor.Motor("MOTOR1", 1)  # Vorne Links
m4 = PiMotor.Motor("MOTOR4", 1)

ab = PiMotor.Arrow(1)
al = PiMotor.Arrow(2)
af = PiMotor.Arrow(3)
ar = PiMotor.Arrow(4)

gpio.setup(trig, gpio.OUT)
gpio.setup(echo, gpio.IN)
gpio.setup(trig2, gpio.OUT)
gpio.setup(echo2, gpio.IN)
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
    m1.stop()
    m2.stop()
    m3.stop()
    m4.stop()


def changeMotors(front, left, right):
    if front > 0:
        if left == 0 and right == 0:
            m1.forward(front)
            m2.forward(front)
            m3.forward(front)
            m4.forward(front)
    if front < 0:
        if left == 0 and right == 0:
            m1.reverse(front * -1)
            m2.reverse(front * -1)
            m3.reverse(front * -1)
            m4.reverse(front * -1)

    if front == 0:
        stopMotors()


async def ir():
    # IR
    with LircdConnection("slidepuzzle", "/home/pi/.lircrc", "/var/run/lirc/lircd") as conn:
        startTime = time.time()
        string = conn.readline()
        if string == "up":
            front = increaseSpeed(front, 20)
            print("Vorwärts")

        if string == "down":
            front = decreaseSpeed(front, 20)
            print("Rückwärts")

        if string == "left":
            left = increaseSpeed(left, 20)
            print("Links")

        if string == "right":
            print("RECHTS")
            right = increaseSpeed(right, 20)

        if string == "ok":
            print("STOP")
            front = 0
            endCondition = False

        print(front)

        changeMotors(front, left, right)
        print("=============")
        # time.sleep(1)
        # endTime = time.time()
        # print(endTime)


async def main():

    endCondition = True
    carPos = CarPosition(0,0,0)
    obstacles = [] # the map, build from points
    lastStop = 0 # seconds since last time the direction was changed
    sensorFront = DistanceSensor(trig, echo, 3)
    sensorLeft = DistanceSensor(trig2, echo2, 3)
    # visual = SlamPlot()

    with open("mapPoints.txt", "w") as f:
        while endCondition:
            lastStop = time.time() # seconds since last time the direction was changed
            first_awaitable = asyncio.create_task(sensorFront.getDistance())
            second_awaitable = asyncio.create_task(sensorLeft.getDistance())

            await ir()

            distanceFront = await first_awaitable
            distanceLeft = await second_awaitable

            print("=============")
            print("Messung")
            print("Front: ", distanceFront)
            print("Left: ", distanceLeft)
            print("=============")

            if distanceFront < 5: # wall in front of car
                front = 0
                left = 0
                right = 1 # ?
                changeMotors(front, left, right) # stop and turn 90 degree right
                carPos.updatePostition(lastStop)
                obstacles.append(carPos.getWallPoint())
                f.write(p + "\n")
            elif distanceLeft < 5: #no wall left of car
                front = 0
                left = 1
                right = 0
                changeMotors(front, left, right) # stop and turn 90 degree left
                carPos.updatePostition(lastStop)
                obstacles.append(carPos.getWallPoint())
                f.write(p + "\n")

    gpio.cleanup()
    # visual.update_plot(obstacles)


asyncio.run(main())

