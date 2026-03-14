import pyverse2d as pv
from pyverse2d import Window, Screen
from pyverse2d import world
from pyverse2d import scene

# Fenêtre OS
screen = Screen()
window = Window(screen=screen, caption="PyVerse2D Demo", vsync=True)
game = pv.set_window(window)

# Scene
camera = scene.Camera()
viewport = scene.Viewport()
main_scene = scene.Scene(camera=camera, viewport=viewport, stack_mode=scene.StackMode.PAUSE)
scene.push(scene=main_scene)

# Monde
main_world = world.World()
world_layer = scene.WorldLayer(world=main_world)
main_scene.add_layer(world_layer)

# Entités
player_shape = pv.shape.Capsule(20, 100)
player = world.Entity(
    world.Transform(pos=pv.math.Point(0.0, 80.0), anchor="center"),
    world.ShapeRenderer(shape=player_shape),
    world.Collider(shape=player_shape),
    world.RigidBody(mass=100.0, friction=0.2, restitution=0.35, linear_damping=0.1)
)
main_world.add_entity(player)

ennemy_shape = pv.shape.Capsule(20, 100)
ennemy = world.Entity(
    world.Transform(pos=pv.math.Point(0.0, 200.0), anchor="center"),
    world.ShapeRenderer(shape=ennemy_shape),
    world.Collider(shape=ennemy_shape),
    world.RigidBody(mass=40.0, friction=0.1, restitution=0.35, linear_damping=0.1)
)
main_world.add_entity(ennemy)

ball_shape = pv.shape.Circle(15.0)
ball = world.Entity(
    world.Transform(pos=pv.math.Point(0.0, 350.0), anchor="center"),
    world.ShapeRenderer(shape=ball_shape),
    world.Collider(shape=ball_shape),
    world.RigidBody(mass=5.0, restitution=0.8)
)
main_world.add_entity(ball)

# Murs
diagonal_shape = pv.shape.Segment((0.0, 0.0), (100.0, 80.0), width=5.0)
diagonal = world.Entity(
    world.Transform(pos=pv.math.Point(-50, -100), anchor="center"),
    world.ShapeRenderer(shape=diagonal_shape),
    world.Collider(shape=diagonal_shape, offset=(0.0, 10.0)),
    world.RigidBody(restitution=0.1)
)
main_world.add_entity(diagonal)

wall_shape = pv.shape.Rect(800, 30)
wall = world.Entity(
    world.Transform(pos=pv.math.Point(-400, -300.0), anchor="center"),
    world.ShapeRenderer(shape=wall_shape),
    world.Collider(shape=wall_shape),
    world.RigidBody(restitution=0.9)
)
main_world.add_entity(wall)

# Systèmes
main_world.add_system(world.RenderSystem())
main_world.add_system(world.PhysicsSystem())
main_world.add_system(world.GravitySystem(gravity=50))
main_world.add_system(world.CollisionSystem())

pv.run()