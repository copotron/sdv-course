import math
import numpy as np #pip install numpy
import skimage #pip install scikit-image

TESLA_MODEL3_WHEEL_BASE = 2.875 #meters

class Robot:
    def __init__(self):
        self.ld = TESLA_MODEL3_WHEEL_BASE
        self.x = 0
        self.y = 0
        self.psi = 0.0 #yaw
        self.v = 0.0
        self.delta = 0.0
        self.a = 0.0

    def move(self, dt):
        x_dot = self.v * np.cos(self.psi)
        y_dot = self.v * np.sin(self.psi)
        psi_dot = self.v * np.tan(self.delta) / self.ld
        v_dot = (-self.v + self.a) / 3 #drag on the car

        self.x += x_dot * dt
        self.y += y_dot * dt
        #self.v += v_dot * dt
        self.psi += psi_dot * dt

    def draw(self, image):
        rr, cc, v = skimage.draw.circle_perimeter_aa(int(self.x), int(self.y), 5)
        image[rr, cc] = 255

