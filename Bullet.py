from Billboard import *
from Texture import *
from math3d import *


class Bullet:
    buffer = None
    size = 0.05

    def __init__(self, origin, direction):
        self.position = origin
        self.lifeTimer = 5
        self.velocity = direction * 15

        if Bullet.buffer is None:
            Bullet.buffer = Billboard(["Resources/bullet.png"], [0], [])

    def hitDetection(self, targetPosition):
        distance = ((self.position.x - targetPosition[0]) ** 2 + (self.position.z - targetPosition[2]) ** 2)
        if distance <= 0.4 ** 2:
            return True
        return False

    def update(self, elapsed, bullets):
        self.position += self.velocity * elapsed
        self.lifeTimer -= elapsed
        if self.lifeTimer <= 0:
            bullets.remove(self)

    @staticmethod
    def draw(shaderManager, bullets):
        locations = []
        for bullet in bullets:
            locations.append(bullet.position[0])
            locations.append(bullet.position[1])
            locations.append(bullet.position[2])

        shaderManager.use()
        Bullet.buffer.setLocations(locations)
        Bullet.buffer.draw(shaderManager, vec2(Bullet.size, Bullet.size))
