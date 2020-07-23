import carla
import time

client = carla.Client('localhost', 2000)
#world = client.get_world()
#print(client.get_available_maps())
world = client.load_world('Town01')

weather = carla.WeatherParameters(
    sun_altitude_angle=70.0)

world.set_weather(weather)

blueprint_library = world.get_blueprint_library()
vehicle_bp = blueprint_library.filter('vehicle.tesla.model3')[0]


transform = carla.Transform()
transform.location.x = 220
transform.location.y = -1.6
transform.location.z = 1.85
transform.rotation.yaw = 180
transform.rotation.pitch = 0
transform.rotation.roll = 0

vehicle = world.spawn_actor(vehicle_bp, transform)

spectator = world.get_spectator()
spectator.set_transform(carla.Transform(transform.location + carla.Location(z=1, x=8), carla.Rotation(yaw=0, pitch=180, roll=180)))

control = carla.VehicleControl()
control.throttle = 0.3
vehicle.apply_control(control)

time.sleep(10)
vehicle.destroy()