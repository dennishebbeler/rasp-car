import numpy as np

class CarPosition:
    """Represents x, y, theta"""

    def __init__(self, x=0.0, y=0.0, theta=0.0):
        super().__init__()

        self.x = x
        self.y = y
        self.theta = theta
    
    def getPosition(self):
        return (self.x, self.y, self.theta)

    def rotate(self, x, y, theta):
        r_x = x * np.cos(theta) - y * np.sin(theta)
        r_y = x * np.sin(theta) + y * np.cos(theta)
        return (r_x, r_y)
        
    def updatePosition(self, timeDriven, rotationChange):
        speed = 10
        speedVector = self.rotate( 0, speed, -self.theta) # align it to the orientation of the car (global to local coordinates)

        self.x += speedVector[0] * timeDriven
        self.y += speedVector[1] * timeDriven
        self.theta = self.normalize_angle(self.theta + rotationChange)

    def normalize_angle(self, angle):
        # normalize the angle so its between 0 and 2 pi
        while angle > 2 * np.pi:
            angle -= 2 * np.pi
        while angle < 0:
            angle += + 2 * np.pi
        return angle

    def getWallPoint(self):
        # placeholder, assumes the wall point is in the local coordinates (-3,-3)
        local = (-3, -3)
        global_x, global_y = self.rotate(local[0] - self.x, local[1] - self.y, self.theta) # change local to global coordinates

        return (global_x, global_y)
        


