from math3d import *
from Mesh import *
import random


class Robot:
    buffer = None

    def __init__(self, origin):
        self.position = origin
        self.velocity = vec3(0, 0, 0)
        self.rotation = 0
        self.setVelocity()
        self.life = 10
        self.alpha = 1
        self.resetTimer = random.randint(2, 10)

        if Robot.buffer is None:
            Robot.buffer = Mesh("Resources/Robot/robot.mesh")

    def setVelocity(self):
        self.velocity = vec3(random.uniform(-1, 1), 0, random.uniform(-1, 1)) * random.uniform(1, 3)
        self.rotation = math.atan(self.velocity.x / self.velocity.z)
        if self.velocity.z <= 0:
            self.rotation += math.pi

    def update(self, bullets, elapsed):
        if self.life <= 0:
            self.alpha -= 1 * elapsed
        else:
            self.resetTimer -= elapsed
            if self.resetTimer <= 0:
                self.resetTimer = random.randint(2, 10)
                self.setVelocity()
            self.position += self.velocity * elapsed
            for bullet in bullets:
                if bullet.hitDetection(self.position):
                    self.life -= 1
                    bullets.remove(bullet)

    def draw(self, shaderManager):
        shaderManager.use()
        shaderManager.setUniform("worldMatrix", axisRotation(vec3(0, 1, 0), self.rotation) * translation(self.position))
        shaderManager.setUniform("alphaOffset", 1 - self.alpha)
        Robot.buffer.draw(shaderManager)
