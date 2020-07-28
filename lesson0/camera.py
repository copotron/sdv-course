import carla
import time
import pygame
import numpy as np

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
sp_transform = carla.Transform(transform.location + carla.Location(z=30, x=-25),
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

    disp.blit(surface, (200,0))
    pygame.display.flip()

display = pygame.display.set_mode(
        (1200, 600),
        pygame.HWSURFACE | pygame.DOUBLEBUF
    )

camera.listen(lambda image: handle_image(display, image))

time.sleep(15)

camera.destroy()
vehicle.destroy()