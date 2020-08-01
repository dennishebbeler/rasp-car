import RPi.GPIO as gpio
import time
from multiprocessing import Value

class DistanceSensor:

    def __init__(self, trig, echo, sensorReadings):
        super().__init__()

        gpio.setmode(gpio.BOARD)
        gpio.setup(trig, gpio.OUT)
        gpio.setup(echo, gpio.IN)
        gpio.output(trig, False) # make sure no signal is sent
        time.sleep(0.5)
        self.trig = trig
        self.echo = echo
        self.sensorReadings = sensorReadings
        self.lastDistance = Value("d", 10.0)
    
    def run(self):
        while True:
            self.lastDistance = self.getDistance()

    def getDistance(self):
        
        readings = [] # take more than 1 reading since sometimes 1 reading can be wrong
        for i in range(self.sensorReadings):
            timeWaited = time.time()

            # pre set in case something goes wrong
            startSensor = time.time()
            stopSensor = time.time()

            gpio.output(self.trig, True)
            time.sleep(0.0001)
            gpio.output(self.trig, False)

            # input(self.echo) is 1 if signal was send but not received
            while gpio.input(self.echo) == 0:
                startSensor = time.time()
                if startSensor > timeWaited + 0.2: #wait at most 0.2 seconds
                    break

            # as soon as the signal is received input(self.echo) becomes 0
            while gpio.input(self.echo) == 1:
                stopSensor = time.time()
                if stopSensor > startSensor + 0.01: #wait at most 0.01 seconds, ca 170 cm
                    break
            
            readings.append(stopSensor - startSensor)

        return sorted(readings)[round(self.sensorReadings/2)] * 17160 # cm 34320/2=17160, sorted list of all readings, take middle one