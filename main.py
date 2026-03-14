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
    world.Transform(pos=pv.math.Point(0.0, 50.0)),
    world.ShapeRenderer(shape=player_shape),
    world.Collider(shape=player_shape),
    world.RigidBody(mass=1.0, friction=0.2, restitution=0.4, linear_damping=0.0)
)
main_world.add_entity(player)

ennemy_shape = pv.shape.Capsule(20, 100)
ennemy = world.Entity(
    world.Transform(pos=pv.math.Point(0.0, 180.0)),
    world.ShapeRenderer(shape=ennemy_shape),
    world.Collider(shape=ennemy_shape),
    world.RigidBody(mass=100.0, friction=0.1, restitution=0.3, linear_damping=0.0)
)
main_world.add_entity(ennemy)

ball_shape = pv.shape.Circle(15.0)
ball = world.Entity(
    world.Transform(pos=pv.math.Point(0.0, 350.0)),
    world.ShapeRenderer(shape=ball_shape),
    world.Collider(shape=ball_shape),
    world.RigidBody(mass=10.0, restitution=0.7)
)
main_world.add_entity(ball)

ellipse_shape = pv.shape.Ellipse(20, 10)
ellipse = world.Entity(
    world.Transform(pos=pv.math.Point(-5.0, 375.0)),
    world.ShapeRenderer(shape=ellipse_shape),
    world.Collider(shape=ellipse_shape),
    world.RigidBody(mass=50, friction=0.1, restitution=0.5)
)
main_world.add_entity(ellipse)

rect_shape = pv.shape.Rect(40, 25)
rect = world.Entity(
    world.Transform(pos=pv.math.Point(5.0, 400)),
    world.ShapeRenderer(rect_shape),
    world.Collider(shape=rect_shape),
    world.RigidBody(mass=5, friction=0.00, restitution=0.2)
)
main_world.add_entity(rect)

segment_shape = pv.shape.Segment(A=(-40, 50), B=(20, -20), width=3.0)
segment = world.Entity(
    world.Transform(pos=pv.math.Point(-100.0, 150.0)),
    world.ShapeRenderer(shape=segment_shape),
    world.Collider(shape=segment_shape),
    world.RigidBody(mass=7.0, friction=0.0, restitution=0.15)
)
main_world.add_entity(segment)

# Murs
diagonal_shape = pv.shape.Segment((0.0, 0.0), (100.0, 80.0), width=5.0)
diagonal = world.Entity(
    world.Transform(pos=pv.math.Point(-50, -100)),
    world.ShapeRenderer(shape=diagonal_shape),
    world.Collider(shape=diagonal_shape, offset=(0.0, 10.0)),
    world.RigidBody(restitution=0.1)
)
main_world.add_entity(diagonal)

wall_shape = pv.shape.Rect(800, 30)
wall = world.Entity(
    world.Transform(pos=pv.math.Point(-400, -300.0)),
    world.ShapeRenderer(shape=wall_shape),
    world.Collider(shape=wall_shape),
    world.RigidBody(restitution=0.9)
)
main_world.add_entity(wall)

# Labels
title_text = pv.asset.Text("Propulsed with PyVerse2D")
title = world.Entity(
    world.Transform(pos=pv.math.Point(0.0, screen.half_height * 0.75)),
    world.TextRenderer(title_text)
)
main_world.add_entity(title)

# Systèmes
main_world.add_system(world.RenderSystem())
main_world.add_system(world.PhysicsSystem(pixels_per_meter=15))
main_world.add_system(world.GravitySystem())
main_world.add_system(world.CollisionSystem())

pv.run()