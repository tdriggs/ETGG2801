from sdl2 import *
from World import *
from Player import *
from Robot import *
from glconstants import *
from glfuncs import *
from sdl2.keycode import *


def debugcallback(source, typ, id_, severity, length, message, obj):
    print(message)


# Create the SDL2 window
SDL_Init(SDL_INIT_VIDEO)
window = SDL_CreateWindow(b"ETGG", 20, 20, 600, 600, SDL_WINDOW_OPENGL)
if not window:
    print("Could not create window")
    raise RuntimeError()

# Initialize SDL2
SDL_GL_SetAttribute(SDL_GL_CONTEXT_PROFILE_MASK, SDL_GL_CONTEXT_PROFILE_CORE)
SDL_GL_SetAttribute(SDL_GL_DEPTH_SIZE, 24)
SDL_GL_SetAttribute(SDL_GL_STENCIL_SIZE, 8)
SDL_GL_SetAttribute(SDL_GL_CONTEXT_MAJOR_VERSION, 3)
SDL_GL_SetAttribute(SDL_GL_CONTEXT_MINOR_VERSION, 3)
SDL_GL_SetAttribute(SDL_GL_CONTEXT_FLAGS, SDL_GL_CONTEXT_DEBUG_FLAG)
SDL_GL_SetAttribute(SDL_GL_CONTEXT_PROFILE_MASK, SDL_GL_CONTEXT_PROFILE_CORE)
SDL_SetRelativeMouseMode(True)
glContext = SDL_GL_CreateContext(window)
if not glContext:
    print("Cannot create GL context")
    raise RuntimeError()

# Initialize the GL Context
glDebugMessageControl(GL_DONT_CARE, GL_DONT_CARE, GL_DONT_CARE, 0, None, 1)
glEnable(GL_DEBUG_OUTPUT_SYNCHRONOUS)
glDebugMessageCallback(debugcallback, None)
glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LEQUAL)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glBlendEquation(GL_FUNC_ADD)
glClearColor(0.2, 0.2, 0.2, 1)

# Specify the shaders to use
billboardShaderManager = ShaderManager("Shaders/billboardVertexShader.txt", "Shaders/billboardFragmentShader.txt")
shaderManager = ShaderManager("Shaders/vertexShader.txt", "Shaders/fragmentShader.txt")

# Set fog
fogType = 1  # 0:Linear, 1:Exponential, 2:Exponential^2
shaderManager.use()
shaderManager.setUniform("fogType", fogType)
billboardShaderManager.use()
billboardShaderManager.setUniform("fogType", fogType)

if fogType == 0:
    fogStart = 5
    fogEnd = 50
    deltaFog = fogEnd - fogStart
    shaderManager.use()
    shaderManager.setUniform("fogStart", fogStart)
    shaderManager.setUniform("deltaFog", deltaFog)
    billboardShaderManager.use()
    billboardShaderManager.setUniform("fogStart", fogStart)
    billboardShaderManager.setUniform("deltaFog", deltaFog)
elif fogType == 1 or fogType == 2:
    fogDensity = 0.25
    shaderManager.use()
    shaderManager.setUniform("fogDensity", fogDensity)
    billboardShaderManager.use()
    billboardShaderManager.setUniform("fogDensity", fogDensity)


# Set light
shaderManager.use()
shaderManager.setUniform("light.color", vec3(1, 1, 1))

# Initialize the object variables
world = World()
player = Player()
robots = []
for i in range(5):
    robots.append(Robot(vec3(4, -1, 4)))

# Initialize the loop variables
keys = set()
last = SDL_GetTicks()
event = SDL_Event()

# Game Loop
done = False
while not done:
    # Update time variables
    now = SDL_GetTicks()
    elapsed = (now - last) / 1000
    last = now

    # Handle input
    while SDL_PollEvent(byref(event)):
        if event.type == SDL_QUIT:
            done = True
        elif event.type == SDL_KEYDOWN:
            k = event.key.keysym.sym
            keys.add(k)
            if k == SDLK_q:
                done = True
        elif event.type == SDL_KEYUP:
            k = event.key.keysym.sym
            keys.discard(k)
        elif event.type == SDL_MOUSEMOTION:
            player.turn(-event.motion.xrel * elapsed)
        elif event.type == SDL_MOUSEBUTTONDOWN:
            player.shoot()

    # Update Player
    if SDLK_w in keys:
        player.walk(0, elapsed)
    if SDLK_s in keys:
        player.walk(0, -elapsed)
    if SDLK_a in keys:
        player.walk(-elapsed, 0)
    if SDLK_d in keys:
        player.walk(elapsed, 0)
    if SDLK_SPACE in keys:
        player.shoot()

    player.update(elapsed)
    world.update(elapsed)

    # Update Fog
    shaderManager.use()
    shaderManager.setUniform("fogCenter", player.position.xyz)
    billboardShaderManager.use()
    billboardShaderManager.setUniform("fogCenter", player.position.xyz)

    # Update Light
    shaderManager.use()
    shaderManager.setUniform("light.position", player.position.xyz)

    # Update Robots
    for robot in robots:
        robot.update(player.gun.bullets, elapsed)
        if robot.alpha <= 0:
            robots.remove(robot)

    # Clear the screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Draw opaque things
    world.draw(shaderManager)
    player.draw(shaderManager, billboardShaderManager)

    # Draw transparent things without the color mask
    glColorMask(0, 0, 0, 0)
    for robot in robots:
        robot.draw(shaderManager)

    # Draw transparent things with the color mask
    glColorMask(1, 1, 1, 1)
    for robot in robots:
        robot.draw(shaderManager)

    # Flip the window buffer
    SDL_GL_SwapWindow(window)

sys.exit(0)
