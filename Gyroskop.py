#!/usr/bin/python
import smbus
import math

class Gyroskop:

    def __init__(self):
                # Register
        self.power_mgmt_1 = 0x6b
        self.power_mgmt_2 = 0x6c

        self.bus = smbus.SMBus(1)  # bus = smbus.SMBus(0) fuer Revision 1
        self.address = 0x68  # via i2cdetect

        # Aktivieren, um das Modul ansprechen zu koennen
        self.bus.write_byte_data(self.address, self.power_mgmt_1, 0)

    def read_byte(self,reg):
        return self.bus.read_byte_data(self.address, reg)


    def read_word(self,reg):
        h = self.bus.read_byte_data(self.address, reg)
        l = self.bus.read_byte_data(self.address, reg + 1)
        value = (h << 8) + l
        return value


    def read_word_2c(self,reg):
        val = self.read_word(reg)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val


    def dist(self,a, b):
        return math.sqrt((a * a) + (b * b))


    def get_y_rotation(self, x, y, z):
        radians = math.atan2(x, self.dist(y, z))
        return -math.degrees(radians)


    def get_x_rotation(self, x, y, z):
        radians = math.atan2(y, self.dist(x, z))
        return math.degrees(radians)

    def getGyroskopX(self,scaled = True):
        gyrosX = self.read_word_2c(0x43)
        if scaled:
            return gyrosX
        else:
            return gyrosX / 131

    def getGyroskopY(self,scaled = True):
        gyrosY = self.read_word_2c(0x45)
        if scaled:
            return gyrosY
        else:
            return gyrosY / 131

    def getGyroskopZ(self,scaled = True):
        gyrosZ = self.read_word_2c(0x47)
        if scaled:
            return gyrosZ
        else:
            return gyrosZ / 131



    def getBeschleunigungX(self,scaled = True):
        beschleunigung_xout = self.read_word_2c(0x3b)
        beschleunigung_xout_skaliert = beschleunigung_xout / 16384.0

        if scaled:
            return beschleunigung_xout
        else:
            return beschleunigung_xout_skaliert

    def getBeschleunigungY(self,scaled = True):
        beschleunigung_yout = self.read_word_2c(0x3d)
        beschleunigung_yout_skaliert = beschleunigung_yout / 16384.0
        if scaled:
            return beschleunigung_yout
        else:
            return beschleunigung_yout_skaliert

    def getBeschleunigungZ(self,scaled = True):
        beschleunigung_zout = self.read_word_2c(0x3f)
        beschleunigung_zout_skaliert = beschleunigung_zout / 16384.0
        if scaled:
            return beschleunigung_zout
        else:
            return beschleunigung_zout_skaliert


