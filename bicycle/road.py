import skimage
import numpy as np

class Road:
    def __init__(self):
        
        rr1, cc1, val = skimage.draw.line_aa(100, 100, 300, 100)        
        rr2, cc2, val = skimage.draw.line_aa(300, 100, 300, 300)
        rr = np.append(rr1, rr2)
        cc = np.append(cc1, cc2)
        self.way_points=[rr, cc]

    def draw(self, image, robot):
        min_points = []
        min_dist = []
        wrr, wcc = self.way_points
        image[wrr, wcc] = 200
        dx = [abs(robot.x-r) for r in wrr]
        dy = [abs(robot.y-c) for c in wcc]
        d = np.hypot(dx, dy)
        midx = np.argmin(d)
        min_points = [wrr[midx], wcc[midx]]

        idx = midx
        if idx < len(self.way_points[0]) - 15:
            idx += 12

        rr, cc, val = skimage.draw.line_aa(int(robot.x), int(robot.y), min_points[0], min_points[1])
        image[rr, cc] = 50

        rr, cc, val = skimage.draw.line_aa(int(robot.x), int(robot.y), wrr[idx], wcc[idx])
        image[rr, cc] = 100
        
                    
