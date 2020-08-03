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

    async def getDistance(self):
        
        readings = [] # take more than 1 reading since sometimes 1 reading can be wrong
        for i in range(self.sensorReadings):
            timeWaited = time.time()

            gpio.output(self.trig, True)
            time.sleep(0.0001)
            gpio.output(self.trig, False)

            startSensor = time.time()
            # input(self.echo) is 1 if signal was send but not received
            while gpio.input(self.echo) == 0:
                startSensor = time.time()
                if startSensor > timeWaited + 0.1: #wait at most 0.1 seconds
                    time.sleep(0.001) # add time so distance is around 17 cm
                    break

            stopSensor = time.time()
            # as soon as the signal is received input(self.echo) becomes 0
            while gpio.input(self.echo) == 1:
                stopSensor = time.time()
                if stopSensor > startSensor + 0.002: #wait at most 0.01 seconds, ca 34 cm
                    break
            
            readings.append(stopSensor - startSensor)
            
            

        return sorted(readings)[round(self.sensorReadings/2)] * 17160 # cm 34320/2=17160, sorted list of all readings, take middle one