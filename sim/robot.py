import numpy as np
import skimage # pip install scikit-image

class Robot:
    def __init__(self):
        self.x = 0
        self.y = 0

        self.psi = 0.0
        self.v = 0.0
        self.delta = 0.0

        self.L = 2.875 # wheel base of tesla model3

    # Implementing bycicle model
    def move(self, dt = 0.1):
        x_dot = self.v * np.cos(self.psi)
        y_dot = self.v * np.sin(self.psi)

        psi_dot = self.v * np.tan(self.delta) / self.L

        self.x = self.x + x_dot * dt
        self.y = self.y + y_dot * dt
        self.psi = self.psi + psi_dot * dt

    def draw(self):
        return skimage.draw.circle_perimeter_aa(int(self.x), int(self.y), 5)
        