import numpy as np

class CarPosition:
    """Represents x, y, theta"""

    def __init__(self, x=0.0, y=0.0, theta=0.0):
        super().__init__()

        self.x = x
        self.y = y
        self.theta = theta
    
    def updatePostition(self, timeDriven, v):
        # velocity of the car * the time driven
        r_x = v[0] * timeDriven
        r_y = v[1] * timeDriven
        r_theta = v[2] * timeDriven

        self.theta = self.normalize_angle(self.theta + r_theta)
        self.x += r_x * np.cos(self.theta) - r_y * np.sin(self.theta)
        self.y += r_x * np.sin(self.theta) + r_y * np.cos(self.theta)

    def normalize_angle(self, angle):
        # normalize the angle so its between pi and -pi
        while angle > np.pi:
            angle = angle - 2 * np.pi
        while angle < -np.pi:
            angle = angle + 2 * np.pi
        return angle

    def getWallPoint(self):
        # placeholder, assumes the wall point is in the local coordinates (-3,-3)
        local = (-3,-3)
        w_x = local[0] * np.cos(self.theta) - local[1] * np.sin(self.theta)
        w_y = local[0] * np.sin(self.theta) + local[1] * np.cos(self.theta)

        return (w_x, w_y)
        

         

