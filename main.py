# ======================================== IMPORTS ========================================
import pyverse2d as pv
from pyverse2d import Window, LogicalScreen, Viewport, Camera
from pyverse2d import world
from pyverse2d import scene

import math

# ======================================== FENÊTRE ========================================
screen = LogicalScreen()
window = Window(screen=screen, caption="PyVerse2D - Demo", vsync=True)
pv.set_window(window)

W = screen.width
H = screen.height
hw = W * 0.5
hh = H * 0.5

# ======================================== SCENE ========================================
camera = Camera(anchor=(0.5, 0.5), view_width=85, view_height=48)
viewport = Viewport(position=(0.0, 0.0), width=1920, height=1080, origin=(0.5, 0.5), direction=(1.0, 1.0))
main_scene = scene.Scene(camera=camera, viewport=viewport, stack_mode=scene.StackMode.PAUSE)
scene.push(scene=main_scene)

main_world = world.World()
world_layer = scene.WorldLayer(world=main_world)
main_scene.add_layer(world_layer, z=0)

# ======================================== PLAYER ========================================
class Player:
    MOVE_FORCE = 2500.0
    AIR_MOVE_FORCE = 500.0
    JUMP_FORCE = 400.0
    MAX_SPEED  = 10.0

    def __init__(self, world_, position):
        self._shape = pv.shape.Capsule(0.65, 4.3)
        img_height = self._shape.height * 96 / (96 - 38)
        self._animation = pv.asset.Animation.from_folder("assets/", prefix="running", framerate=8, height=img_height)
        self._entity = world.Entity(
            world.Transform(position=position, anchor=(0.5, 0.0), rotation=0),
            world.SpriteRenderer(image=pv.asset.Image("assets/idle_0.png", height=img_height), z=15),
            world.Animator(),
            world.Collider(shape=self._shape),
            world.RigidBody(mass=50.0, friction=0.35, restitution=0.1),
            world.GroundSensor(threshold=0.2, ground_damping=4.0, max_step_height=0.75, coyote_time=0.03)
        )
        world_.add_entity(self._entity)
        
        self._animator: world.Animator = self._entity.get(world.Animator)
        self._animator.register(world.Animator.AnimationRequest(self._animation, loop=True, cutable=True, condition=self.is_running))

        self._direction = "right"

    @property
    def entity(self) -> world.Entity:
        return self._entity

    @property
    def rb(self) -> world.RigidBody:
        return self._entity.rigid_body

    @property
    def tr(self) -> world.Transform:
        return self._entity.transform
    
    @property
    def gs(self) -> world.GroundSensor:
        return self._entity.ground_sensor

    @property
    def position(self) -> pv.math.Point:
        return pv.math.Point(self.tr.x, self.tr.y)

    def move_left(self):
        if self.rb.velocity.x > -self.MAX_SPEED:
            self.rb.apply_force(pv.math.Vector(-self.MOVE_FORCE if self.is_grounded() else -self.AIR_MOVE_FORCE, 0.0))
            self._entity.get(world.SpriteRenderer).flip_x = True

    def move_right(self):
        if self.rb.velocity.x < self.MAX_SPEED:
            self.rb.apply_force(pv.math.Vector(self.MOVE_FORCE if self.is_grounded() else self.AIR_MOVE_FORCE, 0.0))
            self._entity.get(world.SpriteRenderer).flip_x = False

    def jump(self):
        if self.is_grounded():
            self.rb.apply_impulse(pv.math.Vector(0.0, self.JUMP_FORCE))

    def is_grounded(self) -> bool:
        return self.gs.is_grounded()
    
    def is_running(self) -> bool:
        return self.is_grounded() and abs(self.rb.velocity.x) > 1.0

# ======================================== STRUCTURE ========================================
r1_shape = pv.shape.Rect(20.0, 1.25)
ramp1 = world.Entity(
    world.Transform(position=pv.math.Point(-15.0, (-hh + 230) / 20), anchor=(0.5, 0.5), rotation=0.0),
    world.ShapeRenderer(shape=r1_shape, filling_color=(139, 90, 43), z=10),
    world.Collider(shape=r1_shape),
    world.RigidBody(restitution=0.1, friction=0.6)
)
main_world.add_entity(ramp1)

r2_shape = pv.shape.Rect(17.5, 1.25)
ramp2 = world.Entity(
    world.Transform(position=pv.math.Point(16.0, (-hh + 250) / 20), anchor=(0.5, 0.5), rotation=-20.0),
    world.ShapeRenderer(shape=r2_shape, filling_color=(139, 90, 43), z=10),
    world.Collider(shape=r2_shape),
    world.RigidBody(restitution=0.1, friction=0.6)
)
main_world.add_entity(ramp2)

p1_shape = pv.shape.Rect(10.0, 1.0)
plat1 = world.Entity(
    world.Transform(position=pv.math.Point(-22.5, 4.0), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=p1_shape, filling_color=(80, 120, 160), z=10),
    world.Collider(shape=p1_shape),
    world.RigidBody(restitution=0.1, friction=0.6)
)
main_world.add_entity(plat1)

p2_shape = pv.shape.Rect(9.0, 1.0)
plat2 = world.Entity(
    world.Transform(position=pv.math.Point(0.0, 0.0), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=p2_shape, filling_color=(80, 120, 160), z=10),
    world.Collider(shape=p2_shape),
    world.RigidBody(restitution=0.1, friction=0.6)
)
main_world.add_entity(plat2)

p3_shape = pv.shape.Rect(8.0, 1.0)
plat3 = world.Entity(
    world.Transform(position=pv.math.Point(22.5, 7.5), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=p3_shape, filling_color=(80, 120, 160), z=10),
    world.Collider(shape=p3_shape),
    world.RigidBody(restitution=0.1, friction=0.6)
)
main_world.add_entity(plat3)

obs1_shape = pv.shape.RegularHexagon(1.75)
obs1 = world.Entity(
    world.Transform(position=pv.math.Point(-7.5, -5.0), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=obs1_shape, filling_color=(60, 60, 80), z=10),
    world.Collider(shape=obs1_shape),
    world.RigidBody(restitution=0.4, friction=0.3)
)
main_world.add_entity(obs1)

obs2_shape = pv.shape.RegularTriangle(2.0)
obs2 = world.Entity(
    world.Transform(position=pv.math.Point(7.5, -5.0), anchor=(0.5, 0.5), rotation=45),
    world.ShapeRenderer(shape=obs2_shape, filling_color=(60, 60, 80), z=10),
    world.Collider(shape=obs2_shape),
    world.RigidBody(restitution=0.4, friction=0.3)
)
main_world.add_entity(obs2)

ball1_shape = pv.shape.Circle(1.0)
ball1 = world.Entity(
    world.Transform(position=pv.math.Point(-20.0, 15.0), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=ball1_shape, filling_color=(80, 180, 220)),
    world.Collider(shape=ball1_shape),
    world.RigidBody(mass=10.0, friction=0.2, restitution=0.75),
)
main_world.add_entity(ball1)

ball2_shape = pv.shape.Circle(0.7)
ball2 = world.Entity(
    world.Transform(position=pv.math.Point(20.0, 15.0), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=ball2_shape, filling_color=(80, 220, 140)),
    world.Collider(shape=ball2_shape),
    world.RigidBody(mass=5.0, friction=0.15, restitution=0.8)
)
main_world.add_entity(ball2)

rect1_shape = pv.shape.Rect(2.75, 2.0)
rect1 = world.Entity(
    world.Transform(position=pv.math.Point(-10.0, 15.0), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=rect1_shape, filling_color=(180, 80, 220)),
    world.Collider(shape=rect1_shape),
    world.RigidBody(mass=40.0, friction=0.5, restitution=0.15)
)
main_world.add_entity(rect1)

rect2_shape = pv.shape.Rect(1.75, 1.25)
rect2 = world.Entity(
    world.Transform(position=pv.math.Point(10.0, 17.5), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=rect2_shape, filling_color=(220, 220, 80)),
    world.Collider(shape=rect2_shape),
    world.RigidBody(mass=8.0, friction=0.4, restitution=0.3)
)
main_world.add_entity(rect2)

ellipse_shape = pv.shape.Ellipse(1.4, 0.7)
ellipse = world.Entity(
    world.Transform(position=pv.math.Point(0.0, 17.5), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=ellipse_shape, filling_color=(80, 220, 220)),
    world.Collider(shape=ellipse_shape),
    world.RigidBody(mass=200.0, friction=0.25, restitution=0.6)
)
main_world.add_entity(ellipse)
ellipse.get(world.RigidBody).apply_force(pv.math.Vector(2000.0, 0.0))

hex1_shape = pv.shape.RegularHexagon(1.25)
hex1 = world.Entity(
    world.Transform(position=pv.math.Point(5.0, 17.5), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=hex1_shape, filling_color=(220, 80, 180)),
    world.Collider(shape=hex1_shape),
    world.RigidBody(mass=18.0, friction=0.45, restitution=0.35)
)
main_world.add_entity(hex1)

tri1_shape = pv.shape.RegularTriangle(1.4)
tri1 = world.Entity(
    world.Transform(position=pv.math.Point(-5.0, 17.5), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=tri1_shape, filling_color=(180, 220, 80)),
    world.Collider(shape=tri1_shape),
    world.RigidBody(mass=12.0, friction=0.3, restitution=0.4)
)
main_world.add_entity(tri1)
tri1.get(world.RigidBody).apply_force(pv.math.Vector(3000.0, 1000.0))

# ======================================== PLAYER ========================================
player = Player(main_world, pv.math.Point(0.0, 10.0))

follower_shape = pv.shape.Circle(1)
follow_image = pv.asset.Image("assets/drone_0.png", height=2.5)
follower = world.Entity(
    world.Transform(position=(50, 0)),
    world.SpriteRenderer(image=follow_image),
    world.Collider(shape=follower_shape),
    world.Follow(player.entity, force=100, radius_min=6, radius_max=7, damping=3, angle=90, cone=60, cone_gap=15),
    world.RigidBody(mass=1, gravity=False)
)
main_world.add_entity(follower)

def follower_update(dt: float) -> None:
    """Actualisation du suiveur"""
    dx = player.entity.transform.position.x - follower.transform.position.x
    if dx >= 0:
        follower.sprite_renderer.flip_x = False
    else:
        follower.sprite_renderer.flip_x = True

# ======================================== CAMERA ========================================
v_left = pv.math.Vector(-0.5, 0)
v_right = pv.math.Vector(0.5, 0)
v_down = pv.math.Vector(0, -0.5)
v_up = pv.math.Vector(0, 0.5)
v_downleft = (v_down + v_left).normalized * 0.5
v_downright = (v_down + v_right).normalized * 0.5
v_upright = (v_up + v_right).normalized * 0.5
v_upleft = (v_up + v_left).normalized * 0.5

def cam_left(): camera.move(v_left)
def cam_right(): camera.move(v_right)
def cam_down(): camera.move(v_down)
def cam_up(): camera.move(v_up)
def cam_downleft(): camera.move(v_downleft)
def cam_downright(): camera.move(v_downright)
def cam_upright(): camera.move(v_upright)
def cam_upleft(): camera.move(v_upleft)

def cam_horizontal() -> int:
    return pv.key.is_pressed(pv.key.K_RIGHT) or pv.key.is_pressed(pv.key.K_LEFT)
def cam_vertical() -> int:
    return pv.key.is_pressed(pv.key.K_UP) or pv.key.is_pressed(pv.key.K_DOWN)

camlock = "free"
def switch_camlock():
    global camlock
    if camlock == "free":
        camlock = "player"
        camera.follow(player._entity.transform, offset=(0, player._shape.height * 0.5), smoothing=0.03)
    else:
        camlock = "free"
        camera.idle()
        camera.goto((0, 0), duration=1.0, easing=pv.math.easing.ease_in_out_quad)

# ======================================== INPUTS ========================================
pv.inputs.add_listener(pv.key.K_F11, window.toggle_fullscreen)

pv.inputs.add_listener(pv.key.K_SPACE, player.jump)
pv.inputs.add_listener(pv.key.K_Q, player.move_left,  repeat=True)
pv.inputs.add_listener(pv.key.K_D, player.move_right, repeat=True)

pv.inputs.add_listener(pv.key.K_LEFT, cam_left, repeat=True, condition=lambda: not cam_vertical())
pv.inputs.add_listener(pv.key.K_RIGHT, cam_right, repeat=True, condition=lambda: not cam_vertical())
pv.inputs.add_listener(pv.key.K_DOWN, cam_down, repeat=True, condition=lambda: not cam_horizontal())
pv.inputs.add_listener(pv.key.K_UP, cam_up, repeat=True, condition=lambda: not cam_horizontal())

pv.inputs.when_all_of([pv.key.K_LEFT, pv.key.K_DOWN], cam_downleft, repeat=True)
pv.inputs.when_all_of([pv.key.K_DOWN, pv.key.K_RIGHT], cam_downright, repeat=True)
pv.inputs.when_all_of([pv.key.K_RIGHT, pv.key.K_UP], cam_upright, repeat=True)
pv.inputs.when_all_of([pv.key.K_UP, pv.key.K_LEFT], cam_upleft, repeat=True)

pv.inputs.add_listener(pv.key.K_L, switch_camlock)
    
# ======================================== SYSTEMS ========================================
main_world.add_system(world.RenderSystem())
main_world.add_system(world.PhysicsSystem())
main_world.add_system(world.GravitySystem(pv.math.Vector(0.0, -9.8)))
main_world.add_system(world.CollisionSystem(slop=0.025, max_position_correction=0.4, extra_iterations_threshold=0.2, restitution_threshold=0.05, restitution_max_velocity=0.5, vel_along_wake_treshold=0.02))
main_world.add_system(world.AnimationSystem())
main_world.add_system(world.SteeringSystem())

# ======================================== MAP ========================================
stage_0 = pv.tile.MapLoader.from_tiled_tmx("map/maps/stage_0.tmx", tile_width=1.5, tile_height=1.5)

# Background
background = stage_0["background"]
background.anchor = (0.5, 0.5)
main_scene.add_layer(pv.scene.TileLayer(background, camera=(background_camera := Camera.derived_from(camera, parallax_x=0.3)), clip_camera=camera), z=-2)

# Parallax
parallax = stage_0["parallax"]
parallax.anchor = (0.5, 0.5)
main_scene.add_layer(pv.scene.TileLayer(parallax, camera=(parallax_camera := Camera.derived_from(camera, parallax_x=0.6)), clip_camera=camera), z=-1)

# Ground
ground = stage_0["ground"]
ground.anchor = (0.5, 0.5)
main_scene.add_layer(pv.scene.TileLayer(ground), z=1)
pv.tile.CollisionMapper(ground).inject(main_world)

# Foreground
foreground = stage_0["foreground"]
foreground.anchor = (0.5, 0.5)
main_scene.add_layer(pv.scene.TileLayer(foreground), z=2)
pv.tile.CollisionMapper(foreground).inject(main_world)

# Bordure
border = stage_0["border"]
border.anchor = (0.5, 0.5)
main_scene.add_layer(pv.scene.TileLayer(border), z=3)
pv.tile.CollisionMapper(border).inject(main_world)

# ======================================== GUI ========================================
gui_layer = pv.scene.GuiLayer(camera=(gui_camera := Camera(anchor=(0, 0))))
main_scene.add_layer(gui_layer, z=50)

back_shape = pv.shape.Rect(500, 200)
back = pv.gui.Surface(
    shape=back_shape,
    position=pv.math.Point(960.0, 540.0),
    anchor=(0.5, 0.5),
    color=(255, 255, 255),
    clipping=True,
)
gui_layer.add(back, name="back", z=0)

text = pv.asset.Text("That's how it works", pv.asset.Font(size=32))
label = pv.gui.Label(
    text=text,
    position=pv.math.Point(0.0, 0.0),
    anchor=pv.math.Point(0.5, 0.5),
    color=pv.asset.Color(0, 0, 0),
)
back.add_child(label, name="label", z=2)

image = pv.asset.Image("map/assets/ground_tile.png", scale_factor=3.0)
sprite = pv.gui.Sprite(
    image=image,
    position=(0.0, 0.0),
    anchor=(0.5, 0.5),
    flip_x=False,
    flip_y=False,
    rotation=45,
    color=(1.0, 0, 0)
)
back.add_child(sprite, name="sprite", z=1)

border = pv.gui.Border(shape=back_shape, position=(0, 0), anchor=(0.5, 0.5), width=1, align="in")
back.add_child(border, "border", z=10)

selection = pv.gui.SelectionGroup(name="my_selection", limit=1, replace=True, deselectable=True)
back.add_behavior(hover_behavior := pv.gui.HoverBehavior())
back.add_behavior(click_behavior := pv.gui.ClickBehavior())
back.add_behavior(select_behavior := pv.gui.SelectBehavior(selection_group=selection))

hover_behavior.add_tween(scale_tween := pv.gui.ScaleTween(target_value=2.0, duration=0))

@hover_behavior.on_enter
def on_hover_enter():
    print("Hover enter")

@hover_behavior.on_leave
def on_hover_leave():
    print("Hover leave")

def on_click():
    print("Clicked")
click_behavior.add(callback=on_click)

@select_behavior.on_select
def on_select():
    print("select")

@select_behavior.on_deselect
def on_deselect():
    print("deselect")

# ======================================== FX ========================================
# Light
light_layer = pv.scene.LightLayer(ambient=0.3, exposure=3.0)
main_scene.add_layer(light_layer, z=-1)

light_layer.add_source(light_point := pv.fx.PointLight(position=player.entity.transform.position.copy(), radius=10, intensity=1.0, falloff=pv.math.easing.ease_out_bounce))
light_point.attach_to(player.entity.transform, offset=(0,  2))

light_layer.add_source(light_cone0 := pv.fx.ConeLight(position=(20.0, 50.0), intensity=1.0, direction=(1.0, -2.0), radius=0.0, angle=15, softness=1.0, falloff=None))
light_layer.add_source(light_cone1 := pv.fx.ConeLight(position=(-20.0, 50.0), intensity=1.0, direction=(-1.0, -2.0), radius=0.0, angle=15, softness=1.0, falloff=None))
light_layer.add_source(light_cone2 := pv.fx.ConeLight(position=(0.0, 50.0), intensity=1.0, direction=(0, -2.0), radius=0.0, angle=15, softness=1.0, falloff=None))

# ======================================== LIFE CYCLE ========================================
def on_update(dt: float):
    """Boucle principale"""
    follower_update(dt)

def on_draw():
    """Boucle d'affichage"""
    light_cone2.direction.x = math.sin(pv.time.timer) * 0.5
    light_cone2.direction.normalize()

# ======================================== LAUNCHING ========================================
pv.preload()
pv.time.target_fps = 900
pv.run(on_update, on_draw)