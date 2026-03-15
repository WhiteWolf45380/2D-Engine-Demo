import pyverse2d as pv
from pyverse2d import Window, Screen
from pyverse2d import world
from pyverse2d import scene

# Fenêtre OS
screen = Screen()
window = Window(screen=screen, caption="PyVerse2D - Physics Showcase", vsync=True)
game = pv.set_window(window)

W = screen.width
H = screen.height
hw = W * 0.5
hh = H * 0.5

# ======================================== SCENE ========================================
camera = scene.Camera()
viewport = scene.Viewport()
main_scene = scene.Scene(camera=camera, viewport=viewport, stack_mode=scene.StackMode.PAUSE)
scene.push(scene=main_scene)

main_world = world.World()
world_layer = scene.WorldLayer(world=main_world)
main_scene.add_layer(world_layer)

# ======================================== STRUCTURE ========================================
# Sol principal
floor_shape = pv.shape.Rect(W * 3, 30)
floor = world.Entity(
    world.Transform(pos=pv.math.Point(0.0, -hh + 15), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=floor_shape, filling_color=(100, 100, 100), z=10),
    world.Collider(shape=floor_shape),
    world.RigidBody(restitution=0.3, friction=0.7)
)
main_world.add_entity(floor)

# Mur gauche
wl_shape = pv.shape.Rect(30, H * 4)
wall_l = world.Entity(
    world.Transform(pos=pv.math.Point(-hw * 3 + 15, 0.0), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=wl_shape, filling_color=(100, 100, 100), z=10),
    world.Collider(shape=wl_shape),
    world.RigidBody(restitution=0.3, friction=0.7)
)
main_world.add_entity(wall_l)

# Mur droit
wr_shape = pv.shape.Rect(30, H * 4)
wall_r = world.Entity(
    world.Transform(pos=pv.math.Point(hw * 3 - 15, 0.0), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=wr_shape, filling_color=(100, 100, 100), z=10),
    world.Collider(shape=wr_shape),
    world.RigidBody(restitution=0.3, friction=0.7)
)
main_world.add_entity(wall_r)

# Plafond
ceil_shape = pv.shape.Rect(W * 3, 30)
ceil = world.Entity(
    world.Transform(pos=pv.math.Point(0.0, hh * 3 - 15), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=ceil_shape, filling_color=(100, 100, 100), z=10),
    world.Collider(shape=ceil_shape),
    world.RigidBody(restitution=0.5, friction=0.3)
)
main_world.add_entity(ceil)

# Rampe gauche douce
r1_shape = pv.shape.Rect(500, 25)
ramp1 = world.Entity(
    world.Transform(pos=pv.math.Point(-400.0, -hh + 160), anchor=(0.5, 0.5), rotation=12.0),
    world.ShapeRenderer(shape=r1_shape, filling_color=(139, 90, 43), z=10),
    world.Collider(shape=r1_shape),
    world.RigidBody(restitution=0.2, friction=0.6)
)
main_world.add_entity(ramp1)

# Rampe droite raide
r2_shape = pv.shape.Rect(400, 25)
ramp2 = world.Entity(
    world.Transform(pos=pv.math.Point(350.0, -hh + 200), anchor=(0.5, 0.5), rotation=-25.0),
    world.ShapeRenderer(shape=r2_shape, filling_color=(139, 90, 43), z=10),
    world.Collider(shape=r2_shape),
    world.RigidBody(restitution=0.2, friction=0.4)
)
main_world.add_entity(ramp2)

# Rampe centrale inversée (crée un V)
r3_shape = pv.shape.Rect(350, 20)
ramp3 = world.Entity(
    world.Transform(pos=pv.math.Point(-50.0, 250), anchor=(0.5, 0.5), rotation=25.0),
    world.ShapeRenderer(shape=r3_shape, filling_color=(139, 90, 43), z=10),
    world.Collider(shape=r3_shape),
    world.RigidBody(restitution=0.3, friction=0.5)
)
main_world.add_entity(ramp3)

# Plateforme haute gauche
p1_shape = pv.shape.Rect(220, 20)
plat1 = world.Entity(
    world.Transform(pos=pv.math.Point(-500.0, 50.0), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=p1_shape, filling_color=(80, 120, 160), z=10),
    world.Collider(shape=p1_shape),
    world.RigidBody(restitution=0.2, friction=0.5)
)
main_world.add_entity(plat1)

# Plateforme haute droite
p2_shape = pv.shape.Rect(180, 20)
plat2 = world.Entity(
    world.Transform(pos=pv.math.Point(480.0, 100.0), anchor=(0.5, 0.5), rotation=-5.0),
    world.ShapeRenderer(shape=p2_shape, filling_color=(80, 120, 160), z=10),
    world.Collider(shape=p2_shape),
    world.RigidBody(restitution=0.2, friction=0.5)
)
main_world.add_entity(plat2)

# Plateforme centrale basse
p3_shape = pv.shape.Rect(150, 20)
plat3 = world.Entity(
    world.Transform(pos=pv.math.Point(0.0, -hh + 350), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=p3_shape, filling_color=(80, 120, 160), z=10),
    world.Collider(shape=p3_shape),
    world.RigidBody(restitution=0.4, friction=0.4)
)
main_world.add_entity(plat3)

# Obstacle hexagonal statique au centre
obs1_shape = pv.shape.RegularHexagon(40)
obs1 = world.Entity(
    world.Transform(pos=pv.math.Point(0.0, -hh + 430), anchor=(0.5, 0.5), rotation=30.0),
    world.ShapeRenderer(shape=obs1_shape, filling_color=(60, 60, 80), z=10),
    world.Collider(shape=obs1_shape),
    world.RigidBody(restitution=0.5, friction=0.3)
)
main_world.add_entity(obs1)

# Obstacle triangle statique droite
obs2_shape = pv.shape.RegularTriangle(50)
obs2 = world.Entity(
    world.Transform(pos=pv.math.Point(250.0, 0.0), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=obs2_shape, filling_color=(60, 60, 80), z=10),
    world.Collider(shape=obs2_shape),
    world.RigidBody(restitution=0.6, friction=0.2)
)
main_world.add_entity(obs2)

# ======================================== OBJETS DYNAMIQUES ========================================

# Grosse capsule — lancée vers la droite
cap1_shape = pv.shape.Capsule(22, 110)
cap1 = world.Entity(
    world.Transform(pos=pv.math.Point(-550.0, 200.0), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=cap1_shape, filling_color=(220, 80, 80)),
    world.Collider(shape=cap1_shape),
    world.RigidBody(mass=60.0, friction=0.3, restitution=0.4)
)
main_world.add_entity(cap1)
cap1.get(world.RigidBody).apply_force(pv.math.Vector(18000.0, 4000.0))

# Capsule légère — gravité réduite, lancée en l'air
cap2_shape = pv.shape.Capsule(12, 60)
cap2 = world.Entity(
    world.Transform(pos=pv.math.Point(400.0, 250.0), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=cap2_shape, filling_color=(220, 140, 80)),
    world.Collider(shape=cap2_shape),
    world.RigidBody(mass=8.0, friction=0.2, restitution=0.6, gravity_scale=0.4)
)
main_world.add_entity(cap2)
cap2.get(world.RigidBody).apply_force(pv.math.Vector(-3000.0, 6000.0))

# Gros cercle très rebondissant
ball1_shape = pv.shape.Circle(28.0)
ball1 = world.Entity(
    world.Transform(pos=pv.math.Point(-300.0, 300.0), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=ball1_shape, filling_color=(80, 180, 220)),
    world.Collider(shape=ball1_shape),
    world.RigidBody(mass=12.0, friction=0.05, restitution=0.95)
)
main_world.add_entity(ball1)
ball1.get(world.RigidBody).apply_force(pv.math.Vector(5000.0, 2000.0))

# Petit cercle très léger — gravité inversée
ball2_shape = pv.shape.Circle(10.0)
ball2 = world.Entity(
    world.Transform(pos=pv.math.Point(100.0, -200.0), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=ball2_shape, filling_color=(80, 220, 140)),
    world.Collider(shape=ball2_shape),
    world.RigidBody(mass=2.0, friction=0.1, restitution=0.85, gravity_scale=-0.6)
)
main_world.add_entity(ball2)
ball2.get(world.RigidBody).apply_force(pv.math.Vector(800.0, -2000.0))

# Cercle moyen — chute libre depuis le haut
ball3_shape = pv.shape.Circle(18.0)
ball3 = world.Entity(
    world.Transform(pos=pv.math.Point(50.0, 350.0), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=ball3_shape, filling_color=(220, 180, 80)),
    world.Collider(shape=ball3_shape),
    world.RigidBody(mass=20.0, friction=0.15, restitution=0.7)
)
main_world.add_entity(ball3)

# Rect lourd — tombe sur la rampe gauche
rect1_shape = pv.shape.Rect(70, 45)
rect1 = world.Entity(
    world.Transform(pos=pv.math.Point(-420.0, 300.0), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=rect1_shape, filling_color=(180, 80, 220)),
    world.Collider(shape=rect1_shape),
    world.RigidBody(mass=80.0, friction=0.5, restitution=0.1)
)
main_world.add_entity(rect1)

# Petit rect — glisse sur la plateforme
rect2_shape = pv.shape.Rect(30, 20)
rect2 = world.Entity(
    world.Transform(pos=pv.math.Point(-480.0, 120.0), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=rect2_shape, filling_color=(220, 220, 80)),
    world.Collider(shape=rect2_shape),
    world.RigidBody(mass=5.0, friction=0.05, restitution=0.3)
)
main_world.add_entity(rect2)

# Rect moyen — lancé horizontalement
rect3_shape = pv.shape.Rect(50, 35)
rect3 = world.Entity(
    world.Transform(pos=pv.math.Point(550.0, 50.0), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=rect3_shape, filling_color=(220, 100, 100)),
    world.Collider(shape=rect3_shape),
    world.RigidBody(mass=30.0, friction=0.3, restitution=0.4)
)
main_world.add_entity(rect3)
rect3.get(world.RigidBody).apply_force(pv.math.Vector(-12000.0, 1000.0))

# Ellipse lourde très glissante
ellipse1_shape = pv.shape.Ellipse(35, 18)
ellipse1 = world.Entity(
    world.Transform(pos=pv.math.Point(-100.0, 350.0), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=ellipse1_shape, filling_color=(80, 220, 220)),
    world.Collider(shape=ellipse1_shape),
    world.RigidBody(mass=100.0, friction=0.1, restitution=0.6)
)
main_world.add_entity(ellipse1)
ellipse1.get(world.RigidBody).apply_force(pv.math.Vector(3000.0, 0.0))

# Ellipse légère — gravité forte
ellipse2_shape = pv.shape.Ellipse(20, 10)
ellipse2 = world.Entity(
    world.Transform(pos=pv.math.Point(300.0, 300.0), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=ellipse2_shape, filling_color=(180, 80, 180)),
    world.Collider(shape=ellipse2_shape),
    world.RigidBody(mass=10.0, friction=0.2, restitution=0.5, gravity_scale=2.5)
)
main_world.add_entity(ellipse2)

# Hexagone dynamique — lancé depuis la gauche
hex1_shape = pv.shape.RegularHexagon(28)
hex1 = world.Entity(
    world.Transform(pos=pv.math.Point(-550.0, -100.0), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=hex1_shape, filling_color=(220, 80, 180)),
    world.Collider(shape=hex1_shape),
    world.RigidBody(mass=20.0, friction=0.3, restitution=0.5)
)
main_world.add_entity(hex1)
hex1.get(world.RigidBody).apply_force(pv.math.Vector(14000.0, 3000.0))

# Hexagone léger — chute depuis le haut avec gravité normale
hex2_shape = pv.shape.RegularHexagon(18)
hex2 = world.Entity(
    world.Transform(pos=pv.math.Point(200.0, 380.0), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=hex2_shape, filling_color=(80, 180, 100)),
    world.Collider(shape=hex2_shape),
    world.RigidBody(mass=8.0, friction=0.25, restitution=0.6)
)
main_world.add_entity(hex2)

# Triangle dynamique — lancé en diagonale
tri1_shape = pv.shape.RegularTriangle(30)
tri1 = world.Entity(
    world.Transform(pos=pv.math.Point(500.0, 350.0), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=tri1_shape, filling_color=(180, 220, 80)),
    world.Collider(shape=tri1_shape),
    world.RigidBody(mass=15.0, friction=0.1, restitution=0.5)
)
main_world.add_entity(tri1)
tri1.get(world.RigidBody).apply_force(pv.math.Vector(-8000.0, 2000.0))

# Triangle très rebondissant — gravité réduite
tri2_shape = pv.shape.RegularTriangle(22)
tri2 = world.Entity(
    world.Transform(pos=pv.math.Point(-200.0, 380.0), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=tri2_shape, filling_color=(100, 200, 220)),
    world.Collider(shape=tri2_shape),
    world.RigidBody(mass=6.0, friction=0.05, restitution=0.9, gravity_scale=0.6)
)
main_world.add_entity(tri2)
tri2.get(world.RigidBody).apply_force(pv.math.Vector(2000.0, 5000.0))

# ======================================== CAMERA ========================================
_cam_t = 0.0
_cam_targets = [
    pv.math.Point(-300.0, 100.0),
    pv.math.Point(300.0, 100.0),
    pv.math.Point(0.0, -200.0),
    pv.math.Point(-200.0, 50.0),
    pv.math.Point(300.0, -100.0),
    pv.math.Point(0.0, 0.0),
]
_cam_idx = 0
_cam_duration = 3.0
_cam_elapsed = 0.0

def _lerp_point(a, b, t):
    t = max(0.0, min(1.0, t))
    ease = t * t * (3.0 - 2.0 * t)
    return pv.math.Point(a.x + (b.x - a.x) * ease, a.y + (b.y - a.y) * ease)

def on_update(dt: float):
    global _cam_elapsed, _cam_idx
    _cam_elapsed += dt
    t = _cam_elapsed / _cam_duration
    src = _cam_targets[_cam_idx]
    dst = _cam_targets[(_cam_idx + 1) % len(_cam_targets)]
    camera.pos = _lerp_point(src, dst, t)
    if _cam_elapsed >= _cam_duration:
        _cam_elapsed = 0.0
        _cam_idx = (_cam_idx + 1) % len(_cam_targets)

# ======================================== SYSTÈMES ========================================
main_world.add_system(world.RenderSystem())
main_world.add_system(world.PhysicsSystem(pixels_per_meter=17))
main_world.add_system(world.GravitySystem())
main_world.add_system(world.CollisionSystem())

pv.run(on_update)