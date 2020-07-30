import carla
import time
import pygame
import numpy as np
import math

from purepursuit import PurePursuit as Controler

client = carla.Client('localhost', 2000)
#print(client.get_available_maps())
world = client.load_world("Town01")

world.set_weather(carla.WeatherParameters.ClearNoon)

bp_lib = world.get_blueprint_library()
vehicle_bp = bp_lib.filter('vehicle.tesla.model3')[0]

transform = carla.Transform()

transform.location.x = 220
transform.location.y = -1.6
transform.location.z = 1.85

transform.rotation.yaw = 180
transform.rotation.pitch = 0
transform.rotation.roll = 0

vehicle = world.spawn_actor(vehicle_bp, transform)

spectator = world.get_spectator()
sp_transform = carla.Transform(transform.location + carla.Location(z=50, x=-25, y=20),
    carla.Rotation(yaw=90, pitch=-90))
spectator.set_transform(sp_transform)

control = carla.VehicleControl()
control.throttle = 0.3
vehicle.apply_control(control)

rgb_camera_bp = world.get_blueprint_library().find('sensor.camera.rgb')
cam_transform = carla.Transform(carla.Location(x=0.8, z=1.7))
camera = world.spawn_actor(rgb_camera_bp, 
    cam_transform,
    attach_to=vehicle,
    attachment_type=carla.AttachmentType.Rigid)

def handle_image(disp, image):
    #image.save_to_disk('output/%05d.png' % image.frame, 
    #   carla.ColorConverter.Raw)
    org_array = np.frombuffer(image.raw_data, dtype=np.dtype('uint8'))
    array = np.reshape(org_array, (image.height, image.width, 4))
    array = array[:, :, :3]
    array = array[:,:,::-1]
    array = array.swapaxes(0,1)
    surface = pygame.surfarray.make_surface(array)

    disp.blit(surface, (0,0))
    pygame.display.flip()

display = pygame.display.set_mode(
        (800, 600),
        pygame.HWSURFACE | pygame.DOUBLEBUF
    )

camera.listen(lambda image: handle_image(display, image))

map = world.get_map()
waypoints = map.generate_waypoints(2.0)
print(len(waypoints))

#for wp in waypoints:
#    world.debug.draw_string(wp.transform.location, "*", life_time=20000, persistent_lines=True)

v_loc = vehicle.get_location()
wp = map.get_waypoint(v_loc, project_to_road=True, lane_type=carla.LaneType.Driving)
t=0
path = [wp]
while t<50:    
    t = t+1
    wp_next = wp.next(2.0)
    if len(wp_next) > 1:
        wp = wp_next[1]
    else:
        wp = wp_next[0]
    path.append(wp)

print(path[0])

prev = path[0]

for wp in path:
    #world.debug.draw_string(wp.transform.location, "X", life_time=20000, persistent_lines=True)
    world.debug.draw_line(prev.transform.location, wp.transform.location, thickness=0.01, color=carla.Color(0,0,255))
    prev = wp

CPS = 10
t=0
while t < 60 * CPS:
    world.debug.draw_string(transform.location + carla.Location(x=5), 
        str(t), life_time=1, persistent_lines=True)    

    if t == 22 * CPS:
        control.steer = -0.3
        vehicle.apply_control(control)
    if t == 26.7 * CPS:
        control.steer = 0
        vehicle.apply_control(control)

    if t >= 35 * CPS:
        control.throttle = -1.0
        control.brake = 1.0
        vehicle.apply_control(control)

    cp = vehicle.get_location()
    wpv = map.get_waypoint(cp, project_to_road=True, lane_type=carla.LaneType.Driving)

    #for i in range(1):
    if True:
        wpv_next = wpv.next(2.0)
        if len(wpv_next) > 1:
            wpv = wpv_next[1]
        else:
            wpv = wpv_next[0]

    #world.debug.draw_line(cp, wpv.transform.location, thickness=0.05, color=carla.Color(255,0,0))

    if True:
        dx = [abs(cp.x - w.transform.location.x) for w in path]
        dy = [abs(cp.y - w.transform.location.y) for w in path]

        #print(dx, dy)
        d = np.hypot(dx,dy)
        ind = np.argmin(d)
        #print(path[ind].transform.location.x, path[ind].transform.location.y, cp.x, cp.y)

    #world.debug.draw_string(wpv.transform.location, "O", life_time=0.3, persistent_lines=True)
    world.debug.draw_string(path[ind].transform.location, "O", life_time=0.3, persistent_lines=True)
    world.debug.draw_string(cp, "X", life_time=0.3, persistent_lines=True)
    #print(cp.x, cp.y)

    time.sleep(1.0/CPS)
    t=t+1

camera.destroy()
vehicle.destroy()