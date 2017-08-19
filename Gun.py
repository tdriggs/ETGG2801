from Mesh import *
from Bullet import *


class Gun:
    buffer = None

    def __init__(self, origin, lookVector):
        self.position = vec3(0, 0, 0)
        self.lookVector = vec3(0, 0, 0)
        self.positionMatrix = mat4(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.initialMatrix = math3d.scaling(vec3(0.25, 0.25, 0.25)) * axisRotation(vec3(1, 0, 0), math.pi / 2) * translation(vec3(0, -0.25, 1))
        self.updatePosition(origin, lookVector)

        self.bullets = []
        self.addBullet()
        self.bullets = []

        if Gun.buffer is None:
            Gun.buffer = Mesh("Resources/Raygun/raygun.mesh")

    def addBullet(self):
        start = self.position + (self.lookVector * 1) + vec4(0, -0.25, 0, 0)
        self.bullets.append(Bullet(start, self.lookVector))

    def updatePosition(self, position, lookVector):
        self.position = position
        self.lookVector = lookVector
        rotation = math.atan(self.lookVector.x / self.lookVector.z)
        if self.lookVector.z <= 0:
            rotation += math.pi
        self.positionMatrix = self.initialMatrix * axisRotation(vec3(0, 1, 0), rotation) * translation(self.position)

    def update(self, elapsed, position, lookVector):
        self.updatePosition(position, lookVector)

        for b in self.bullets:
            b.update(elapsed, self.bullets)

    def draw(self, shaderManager, billboardShaderManager):
        shaderManager.use()
        shaderManager.setUniform("worldMatrix", self.positionMatrix)
        Gun.buffer.draw(shaderManager)

        billboardShaderManager.use()
        billboardShaderManager.setUniform("worldMatrix", translation(vec3(0, 0, 0)))
        Bullet.draw(billboardShaderManager, self.bullets)
