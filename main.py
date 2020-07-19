import RPi.GPIO as gpio
import lirc
import time
from lirc import LircdConnection

gpio.setmode(gpio.BCM)
pirSensor = 21
lichtStatus = False
warteZeit = 60*15

bootTime = time.time()

print(bootTime)

# IR
with LircdConnection("slidepuzzle", "/home/pi/.lircrc", "/var/run/lirc/lircd") as conn:
    while True:
        startTime = time.time() 
        string = conn.readline()
        print(string)
        if string == "up":
            print("Vorwärts")
        if string == "down":
            print("Rückwärts")
        if string == "left":
            print("Links")
        if string == "right":
            print("RECHTS")
            
        endTime = time.time()
        print(endTime);


