import skimage
import numpy as np

class Environment:
    def __init__(self):
        rr0, cc0, vv = skimage.draw.line_aa(100,100, 300, 100)
        rr1, cc1, vv1 = skimage.draw.line_aa(300,100, 300, 300)
        rr2, cc2, vv2 = skimage.draw.line_aa(300,300, 100, 100)

        rr = np.append(np.append(rr0, rr1), rr2)
        cc = np.append(np.append(cc0, cc1), cc2)

        self.way_points = [rr, cc]

    def draw(self):
        return self.way_points