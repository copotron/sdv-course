import skimage
import numpy as np

class Road:
    def __init__(self):
        
        rr1, cc1, val = skimage.draw.line_aa(100, 100, 300, 100)        
        rr2, cc2, val = skimage.draw.line_aa(300, 100, 300, 300)
        rr3, cc3, val = skimage.draw.line_aa(300, 300, 500, 350)
        rr4, cc4, val = skimage.draw.line_aa(500, 350, 100, 350)
        rr5, cc5, val = skimage.draw.line_aa(100, 350, 100, 100)

        #rr5, cc5 = skimage.draw.bezier_curve(100, 350, 150, 170, 100, 120, 8)
        rr = np.append(rr1, np.append(np.append(np.append(rr2, rr3), rr4), rr5))
        cc = np.append(cc1, np.append(np.append(np.append(cc2, cc3), cc4), cc5))
        self.way_points=[rr, cc]

    def get_target_points(self, robot):
        min_points = []
        min_dist = []
        wrr, wcc = self.way_points        
        dx = [abs(robot.x-r) for r in wrr]
        dy = [abs(robot.y-c) for c in wcc]
        d = np.hypot(dx, dy)
        midx = np.argmin(d)
        min_points = [wrr[midx], wcc[midx]]

        idx = midx
        if idx < len(self.way_points[0]) - 15:
            idx += 12

        return [(wrr[idx], wcc[idx]), (min_points[0], min_points[1])]

    def draw(self, image, robot):
        wrr, wcc = self.way_points
        image[wrr, wcc] = 200

        (tx, ty), (mx, my) = self.get_target_points(robot)

        rr, cc, val = skimage.draw.line_aa(int(robot.x), int(robot.y), mx, my)
        image[rr, cc] = 50

        rr, cc, val = skimage.draw.line_aa(int(robot.x), int(robot.y), tx, ty)
        image[rr, cc] = 100
        
                    
