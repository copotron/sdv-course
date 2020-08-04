import math
import numpy as np

class PurePursuit:
    def get_target_point(self, waypoints, rx, ry, ld):

        wr, wc = waypoints
        dx = [abs(rx-r) for r in wr]
        dy = [abs(ry-c) for c in wc]

        d = np.hypot(dx,dy)
        minidx = np.argmin(d)        

        idx = minidx
        if idx < len(wr) - ld -1:
            idx += ld

        return [(wr[idx], wc[idx]), (wr[minidx], wc[minidx])]

    def get_control(self, waypoints, L, rx, ry, psi, ld=12):
        (tx, ty), (mx, my) = self.get_target_point(waypoints, 
            rx, ry, ld)
        
        alpha = math.atan2(ty-ry, tx-rx) - psi
        delta = math.atan2(2*L*math.sin(alpha)/ld, 1.0)

        return delta