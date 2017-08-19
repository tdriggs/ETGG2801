from Camera import *
from Bullet import *
from Gun import *


class Player:
    def __init__(self):
        self.position = 0
        self.lookVector = 0
        self.upVector = 0
        self.rightVector = 0
        self.speed = 10
        self.turnSpeed = 0.5

        self.cam = Camera(vec3(2, 0, 2), vec3(4, 0, 4))
        self.updatePosition()

        self.gun = Gun(self.position, self.lookVector)

    def turn(self, angle):
        self.cam.turn(angle * self.turnSpeed)

    def walk(self, distanceX, distanceZ):
        self.cam.move(distanceX * self.speed, 0, distanceZ * self.speed)

    def shoot(self):
        self.gun.addBullet()

    def updatePosition(self):
        self.position = self.cam.eye
        self.lookVector = -self.cam.W
        self.upVector = self.cam.V
        self.rightVector = self.cam.U

    def update(self, elapsed):
        self.gun.update(elapsed, self.position, self.lookVector)
        self.updatePosition()

    def draw(self, shaderManager, billboardShaderManager):
        self.gun.draw(shaderManager, billboardShaderManager)

        shaderManager.use()
        self.cam.draw(shaderManager, billboardShaderManager)
