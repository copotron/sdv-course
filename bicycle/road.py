import skimage
import numpy as np

class Road:
    def __init__(self):
        self.way_points=[]
        rr, cc, val = skimage.draw.line_aa(100, 100, 300, 100)
        self.way_points.append((rr, cc))
        rr, cc, val = skimage.draw.line_aa(300, 100, 300, 300)
        self.way_points.append((rr, cc)) # todo marge the waypoints rr, cc into 2 values instead of 4        

    def draw(self, image, robot):
        min_points = []
        min_dist = []
        for wp in self.way_points:
            rr, cc = wp
            image[rr, cc] = 200
            dx = [abs(robot.x-r) for r in rr]
            dy = [abs(robot.y-c) for c in cc]
            d = np.hypot(dx, dy)
            midx = np.argmin(d)
            min_points.append([rr[midx], cc[midx]])
            min_dist.append(d[midx])
        
        #print(min_points)
        #for mp in min_points:
        #    print(mp, "--", mp[1], mp[2])
        #    rr, cc, val = skimage.draw.line_aa(int(robot.x), int(robot.y), mp[1], mp[2])
        #    image[rr, cc] = 255

        mdi = np.argmin(min_dist)
        print(mdi)
        mp = min_points[mdi]

        rr, cc, val = skimage.draw.line_aa(int(robot.x), int(robot.y), mp[0], mp[1])
        image[rr, cc] = 50



                    
