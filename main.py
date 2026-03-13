import pyverse2d as pv
from pyverse2d import Window, Screen
from pyverse2d import world
from pyverse2d import scene

# Fenêtre OS
screen = Screen()
window = Window(screen=screen, title="PyVerse2D Demo", vsync=True)
game = pv.set_window(window)

# Scene
camera = scene.Camera()
viewport = scene.Viewport()
main_scene = scene.Scene(camera=camera, viewport=viewport)
scene.push(scene=main_scene, mode=scene.StackMode.PAUSE)

# Monde
main_world = world.World()
world_layer = scene.WorldLayer(world=main_world)

# Entités
player_shape = pv.shape.Capsule(20, 100)
player = world.Entity(
    world.Transform(pos=pv.math.Point(0.0, 0.0), anchor="center"),
    world.ShapeRenderer(shape=player_shape),
    world.Collider(shape=player_shape),
    world.RigidBody(mass=60.0)
)
main_world.add_entity(player)

# Systèmes
main_world.add_system(world.RenderSystem())

pv.run()