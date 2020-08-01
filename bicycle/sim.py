import time
import pygame
import numpy as np

from robot import Robot
from road import Road

def main():    
    pygame.init()
    pygame.display.set_caption("Self driving vehicle")
     
    display = pygame.display.set_mode((800,600), pygame.HWSURFACE | pygame.DOUBLEBUF)    
        
    x = np.arange(0, 600)
    y = np.arange(0, 800)
    X, Y = np.meshgrid(x, y)
    Z = X + Y
    Z = 255*Z/Z.max()

    def get_image(t, robot, road):
        Z = np.zeros((800,600), dtype=np.uint8)
        robot.draw(Z)
        road.draw(Z, robot)
        surf = pygame.surfarray.make_surface(Z)
        return surf

    robot = Robot()
    robot.x = 150
    robot.y = 150
    robot.v = 30
    robot.delta = 0.02

    road = Road()

    t = 0
    dt = 0.1
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False     

        robot.move(dt)
        surf = get_image(t, robot, road)
        display.blit(surf, (0, 0))
        pygame.display.flip()
        time.sleep(0.033)
        t+=1

if __name__=="__main__":
    main()
