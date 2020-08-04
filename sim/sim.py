import time
import pygame
import numpy as np
from robot import Robot
from environment import Environment
from purepursuit import PurePursuit

def get_surface(env, robot):
    image = np.zeros((800,600), dtype=np.uint8)

    rr, cc = env.draw()
    image[rr, cc] = 200

    r, c, v = robot.draw()
    image[r,c] = 255

    surface = pygame.surfarray.make_surface(image)
    return surface

def main():
    pygame.init()
    pygame.display.set_caption("Autonomous Vehicle Simulator")

    display = pygame.display.set_mode((800,600), 
        pygame.HWSURFACE | pygame.DOUBLEBUF)

    robot = Robot()
    robot.x = 300
    robot.y = 300
    robot.v = 50.0
    robot.delta = 0.05

    env = Environment()
    controller = PurePursuit()

    dt = 0.1
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        delta = controller.get_control(env.way_points, 
            robot.L, robot.x, robot.y, robot.psi, 12)
        robot.delta = delta
        robot.move(dt)
        surf = get_surface(env, robot)        
        display.blit(surf, (0,0))
        pygame.display.flip()

        time.sleep(dt)

if __name__=="__main__":
    main()