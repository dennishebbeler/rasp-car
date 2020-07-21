import RPi.GPIO as gpio
import lirc
import time
import asyncio
from MotorShield import PiMotor
from lirc import LircdConnection

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

async def distanceSensor():
    gpio.setmode(gpio.BOARD)
    gpio.setup(trig, gpio.OUT)
    gpio.setup(echo, gpio.IN)
    gpio.setup(trig2, gpio.OUT)
    gpio.setup(echo2, gpio.IN)
    print("=============")
    gpio.output(trig, False)

    time.sleep(5)
    gpio.output(trig, True)
    time.sleep(0.0001)
    gpio.output(trig, False)

    startSensor = time.time()

    while gpio.input(echo) == 0:
        startSensor = time.time()

    while gpio.input(echo) == 1:
        stopSensor = time.time()

    vergangeneZeit = stopSensor - startSensor
    entfernung = round(vergangeneZeit * 34000 / 2, 2)
    distance1 = entfernung
    print(distance1)
    print("=============")
    return distance1


async def distanceSensor2():
    gpio.setmode(gpio.BOARD)
    gpio.setup(trig, gpio.OUT)
    gpio.setup(echo, gpio.IN)
    gpio.setup(trig2, gpio.OUT)
    gpio.setup(echo2, gpio.IN)
    print("=============")
    gpio.output(trig2, False)

    time.sleep(5)
    gpio.output(trig2, True)
    time.sleep(0.0001)
    gpio.output(trig2, False)

    startSensor = time.time()

    while gpio.input(echo2) == 0:
        startSensor = time.time()

    while gpio.input(echo2) == 1:
        stopSensor = time.time()

    vergangeneZeit = stopSensor - startSensor
    entfernung = round(vergangeneZeit * 34000 / 2, 2)
    distance2 = entfernung
    print(distance2)
    return distance2


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
    while endCondition:
        first_awaitable = asyncio.create_task(distanceSensor())
        second_awaitable = asyncio.create_task(distanceSensor2())

        await ir()

        distance1 = await first_awaitable
        distance2 = await second_awaitable

        print("=============")
        print("Messung")
        print(distance1)
        print(distance2)
        print("=============")

        if distance1 < 2 or distance2 < 2:
            front = 0
            left = 0
            right = 0
            changeMotors(front, left, right)

    gpio.cleanup()


asyncio.run(main())

