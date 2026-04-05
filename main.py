import pyverse2d as pv
from pyverse2d import Window, Screen
from pyverse2d import world
from pyverse2d import scene
import gc

# ======================================== FENÊTRE ========================================
screen = Screen()
window = Window(screen=screen, caption="PyVerse2D - Player Demo", vsync=True)
pv.set_window(window)

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
main_scene.add_layer(world_layer, z=0)

# ======================================== PLAYER ========================================
class Player:
    MOVE_FORCE = 2500.0
    AIR_MOVE_FORCE = 500.0
    JUMP_FORCE = 400.0
    MAX_SPEED  = 10.0

    def __init__(self, world_, position):
        self._shape = pv.shape.Capsule(18, 80)
        self._animation = pv.asset.Animation.from_folder("assets/", prefix="running", framerate=8, scale_factor=1.4)
        self._entity = world.Entity(
            world.Transform(position=position, anchor=(0.5, 0.0)),
            world.SpriteRenderer(image=pv.asset.Image("assets/idle_0.png", scale_factor=1.4), z=15),
            world.ShapeRenderer(shape=self._shape),
            world.Animator(),
            world.Collider(shape=self._shape),
            world.RigidBody(mass=50.0, friction=0.35, restitution=0.1),
            world.GroundSensor(threshold=0.2, ground_damping=4.0, max_step_height=20)
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
r1_shape = pv.shape.Rect(400, 25)
ramp1 = world.Entity(
    world.Transform(position=pv.math.Point(-300.0, -hh + 230), anchor=(0.5, 0.5), rotation=0.0),
    world.ShapeRenderer(shape=r1_shape, filling_color=(139, 90, 43), z=10),
    world.Collider(shape=r1_shape),
    world.RigidBody(restitution=0.1, friction=0.6)
)
main_world.add_entity(ramp1)

r2_shape = pv.shape.Rect(350, 25)
ramp2 = world.Entity(
    world.Transform(position=pv.math.Point(320.0, -hh + 250), anchor=(0.5, 0.5), rotation=-20.0),
    world.ShapeRenderer(shape=r2_shape, filling_color=(139, 90, 43), z=10),
    world.Collider(shape=r2_shape),
    world.RigidBody(restitution=0.1, friction=0.6)
)
main_world.add_entity(ramp2)

p1_shape = pv.shape.Rect(200, 20)
plat1 = world.Entity(
    world.Transform(position=pv.math.Point(-450.0, 80.0), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=p1_shape, filling_color=(80, 120, 160), z=10),
    world.Collider(shape=p1_shape),
    world.RigidBody(restitution=0.1, friction=0.6)
)
main_world.add_entity(plat1)

p2_shape = pv.shape.Rect(180, 20)
plat2 = world.Entity(
    world.Transform(position=pv.math.Point(0.0, 0.0), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=p2_shape, filling_color=(80, 120, 160), z=10),
    world.Collider(shape=p2_shape),
    world.RigidBody(restitution=0.1, friction=0.6)
)
main_world.add_entity(plat2)

p3_shape = pv.shape.Rect(160, 20)
plat3 = world.Entity(
    world.Transform(position=pv.math.Point(450.0, 150.0), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=p3_shape, filling_color=(80, 120, 160), z=10),
    world.Collider(shape=p3_shape),
    world.RigidBody(restitution=0.1, friction=0.6)
)
main_world.add_entity(plat3)

obs1_shape = pv.shape.RegularHexagon(35)
obs1 = world.Entity(
    world.Transform(position=pv.math.Point(-150.0, -100), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=obs1_shape, filling_color=(60, 60, 80), z=10),
    world.Collider(shape=obs1_shape),
    world.RigidBody(restitution=0.4, friction=0.3)
)
main_world.add_entity(obs1)

obs2_shape = pv.shape.RegularTriangle(40)
obs2 = world.Entity(
    world.Transform(position=pv.math.Point(150.0, -100.0), anchor=(0.0, 0.0), rotation=45),
    world.ShapeRenderer(shape=obs2_shape, filling_color=(60, 60, 80), z=10),
    world.Collider(shape=obs2_shape),
    world.RigidBody(restitution=0.4, friction=0.3)
)
main_world.add_entity(obs2)

# Objets dynamiques
ball1_shape = pv.shape.Circle(20.0)
ball1 = world.Entity(
    world.Transform(position=pv.math.Point(-400.0, 300.0), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=ball1_shape, filling_color=(80, 180, 220)),
    world.Collider(shape=ball1_shape),
    world.RigidBody(mass=10.0, friction=0.2, restitution=0.75)
)
main_world.add_entity(ball1)
ball1.get(world.RigidBody).apply_force(pv.math.Vector(6000.0, 0.0))

ball2_shape = pv.shape.Circle(14.0)
ball2 = world.Entity(
    world.Transform(position=pv.math.Point(400.0, 300.0), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=ball2_shape, filling_color=(80, 220, 140)),
    world.Collider(shape=ball2_shape),
    world.RigidBody(mass=5.0, friction=0.15, restitution=0.8)
)
main_world.add_entity(ball2)
ball2.get(world.RigidBody).apply_force(pv.math.Vector(-4000.0, 2000.0))

rect1_shape = pv.shape.Rect(55, 40)
rect1 = world.Entity(
    world.Transform(position=pv.math.Point(-200.0, 300.0), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=rect1_shape, filling_color=(180, 80, 220)),
    world.Collider(shape=rect1_shape),
    world.RigidBody(mass=40.0, friction=0.5, restitution=0.15)
)
main_world.add_entity(rect1)

rect2_shape = pv.shape.Rect(35, 25)
rect2 = world.Entity(
    world.Transform(position=pv.math.Point(200.0, 350.0), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=rect2_shape, filling_color=(220, 220, 80)),
    world.Collider(shape=rect2_shape),
    world.RigidBody(mass=8.0, friction=0.4, restitution=0.3)
)
main_world.add_entity(rect2)

ellipse_shape = pv.shape.Ellipse(28, 14)
ellipse = world.Entity(
    world.Transform(position=pv.math.Point(0.0, 350.0), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=ellipse_shape, filling_color=(80, 220, 220)),
    world.Collider(shape=ellipse_shape),
    world.RigidBody(mass=200.0, friction=0.25, restitution=0.6)
)
main_world.add_entity(ellipse)
ellipse.get(world.RigidBody).apply_force(pv.math.Vector(2000.0, 0.0))

hex1_shape = pv.shape.RegularHexagon(25)
hex1 = world.Entity(
    world.Transform(position=pv.math.Point(100.0, 350.0), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=hex1_shape, filling_color=(220, 80, 180)),
    world.Collider(shape=hex1_shape),
    world.RigidBody(mass=18.0, friction=0.45, restitution=0.35)
)
main_world.add_entity(hex1)

tri1_shape = pv.shape.RegularTriangle(28)
tri1 = world.Entity(
    world.Transform(position=pv.math.Point(-100.0, 350.0), anchor=(0.5, 0.5)),
    world.ShapeRenderer(shape=tri1_shape, filling_color=(180, 220, 80)),
    world.Collider(shape=tri1_shape),
    world.RigidBody(mass=12.0, friction=0.3, restitution=0.4)
)
main_world.add_entity(tri1)
tri1.get(world.RigidBody).apply_force(pv.math.Vector(3000.0, 1000.0))

# ======================================== PLAYER ========================================
player = Player(main_world, pv.math.Point(0.0, 200.0))

# ======================================== CAMERA ========================================
def cam_left(): camera.move(pv.math.Vector(-10, 0))
def cam_right(): camera.move(pv.math.Vector(10, 0))
def cam_down(): camera.move(pv.math.Vector(0, -10))
def cam_up(): camera.move(pv.math.Vector(0, 10))

camlock = "free"
def switch_camlock():
    global camlock
    if camlock == "free":
        camlock = "player"
        camera.follow(player._entity, smoothing=0.03)
        camera.offset = pv.math.Vector(0.0, 30)
    else:
        camlock = "free"
        camera.unfollow()
        camera.offset = pv.math.Vector(0.0, 0.0)
        camera.goto((0, 0), duration=1.0, easing=pv.math.easing.ease_in_out_quad)

# ======================================== INPUTS ========================================
pv.inputs.add_listener(pv.key.K_SPACE, player.jump)
pv.inputs.add_listener(pv.key.K_Q, player.move_left,  repeat=True)
pv.inputs.add_listener(pv.key.K_D, player.move_right, repeat=True)

pv.inputs.add_listener(pv.key.K_LEFT, cam_left, repeat=True)
pv.inputs.add_listener(pv.key.K_RIGHT, cam_right, repeat=True)
pv.inputs.add_listener(pv.key.K_DOWN, cam_down, repeat=True)
pv.inputs.add_listener(pv.key.K_UP, cam_up, repeat=True)

pv.inputs.add_listener(pv.key.K_L, switch_camlock)
    
# ======================================== SYSTEMS ========================================
main_world.add_system(world.RenderSystem())
main_world.add_system(world.PhysicsSystem(pixels_per_meter=25))
main_world.add_system(world.GravitySystem(pv.math.Vector(0.0, -9.8)))
main_world.add_system(world.CollisionSystem())
main_world.add_system(world.AnimationSystem())

# ======================================== MAP ========================================
stage_0 = pv.tile.MapLoader.from_tiled_tmx("map/maps/stage_0.tmx", tile_width=32, tile_height=32)

# Background
background = stage_0["background"]
background.anchor = (0.5, 0.5)
main_scene.add_layer(pv.scene.TileLayer(background, parallax=(0.5, 1.0), parallax_clamp=True), z=-2)

# Parallax
parallax = stage_0["parallax"]
parallax.anchor = (0.5, 0.5)
main_scene.add_layer(pv.scene.TileLayer(parallax, parallax=(0.6, 1.0), parallax_clamp=True), z=-1)

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
gui_layer = pv.scene.GuiLayer(camera_mode=pv.scene.CameraMode.SCREEN)
main_scene.add_layer(gui_layer, z=50)

back_shape = pv.shape.Rect(500, 200)
back = pv.gui.Surface(
    shape=back_shape,
    position=pv.math.Point(0.0, 0.0),
    anchor=(0.5, 0.5),
    color=(255, 255, 255),
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
    flip_x=True,
    flip_y=True,
    rotation=45,
    color=(1.0, 0, 0)
)
back.add_child(sprite, name="sprite", z=1)

border = pv.gui.Border(shape=back_shape, position=(0, 0), anchor=(0.5, 0.5), width=10)
gui_layer.add(border, "border", z=10)

selection = pv.gui.SelectionGroup(name="my_selection", limit=1, replace=True, deselectable=True)
back.add_behavior(hover_behavior := pv.gui.HoverBehavior())
back.add_behavior(click_behavior := pv.gui.ClickBehavior())
back.add_behavior(select_behavior := pv.gui.SelectBehavior(selection_group=selection))

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

# ======================================== UPDATE ========================================
def on_update(dt: float):
    """Boucle principale"""
    pass

main_scene.preload()
gc.disable()
pv.time.target_fps = 90
pv.run(on_update)