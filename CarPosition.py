import numpy as np

class CarPosition:
    """Represents x, y, theta"""

    def __init__(self, x=0.0, y=0.0, theta=0.0):
        super().__init__()

        self.x = x
        self.y = y
        self.theta = theta
    
    def getVelocity(self, timeDriven, speed):
        v = (0,0,0)
        distance = timeDriven * speed
        if self.theta == 0:
            v = (0, distance, 0)
        elif self.theta == 0.5 * np.pi:
            v = (distance, 0, self.theta)
        elif self.theta == np.pi:
            v = (0, -distance, self.theta)
        elif self.theta == 1.5 * np.pi:
            v = (-distance, 0, self.theta)
        return v

    def updatePostition(self, timeDriven):
        # velocity of the car * the time driven
        speed = 1.2
        v = self.getVelocity(timeDriven, speed)
        r_x = v[0] * timeDriven
        r_y = v[1] * timeDriven
        r_theta = v[2] * timeDriven

        self.theta = self.normalize_angle(self.theta + r_theta)
        self.x += r_x * np.cos(self.theta) - r_y * np.sin(self.theta)
        self.y += r_x * np.sin(self.theta) + r_y * np.cos(self.theta)

    def normalize_angle(self, angle):
        # normalize the angle so its between 0 and 2 pi
        while angle > 2 * np.pi:
            angle -= 2 * np.pi
        while angle < 0:
            angle += + 2 * np.pi
        return angle

    def getWallPoint(self):
        # placeholder, assumes the wall point is in the local coordinates (-3,-3)
        local = (-3,-3)
        global_x = local[0] * np.cos(self.theta) - local[1] * np.sin(self.theta) + self.x
        global_y = local[0] * np.sin(self.theta) + local[1] * np.cos(self.theta) + self.y

        return (global_x, global_y)
        

         

