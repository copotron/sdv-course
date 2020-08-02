import math

class PurePursuit:
    def apply_control(self, robot, road):
        (tx, ty), (mx, my) = road.get_target_points(robot)
        alpha = math.atan2(ty-robot.y, tx-robot.x) - robot.psi
        delta = math.atan2(2*robot.ld * math.sin(alpha)/12, 1.0)

        robot.delta = delta