import BottomSquare
import Cube
import TopSquare
from Texture import *
from math3d import *


class World:
    blockBuffer = None
    ceilingBuffer = None
    floorBuffer = None
    blockPositions = []
    floorPositions = []
    ceilingPositions = []
    blockIndices = []
    floorIndices = []
    ceilingIndices = []

    def __init__(self):
        self.blockTextures = ["Resources/brick.png", "Resources/brick2.png", "Resources/brick3.png", "Resources/brick4.png"]
        self.floorTextures = ["Resources/floor.png", "Resources/floor2.png"]
        self.ceilingTextures = ["Resources/ceiling.png", "Resources/ceiling2.png", "Resources/ceiling3.png"]

        self.readData()

        self.animateTimer = 0
        self.animateTime = 1

        World.blockBuffer = Cube.Cube(self.blockTextures, World.blockIndices, World.blockPositions)
        World.floorBuffer = BottomSquare.BottomSquare(self.floorTextures, World.floorIndices, World.floorPositions)
        World.ceilingBuffer = TopSquare.TopSquare(self.ceilingTextures, World.ceilingIndices, World.ceilingPositions)

    def readData(self):
        file = open("Resources/world.txt", "r")
        currentBlockIndex = 0
        currentCeilingIndex = 0
        currentFloorIndex = 0
        zOffset = 0
        for line in file:
            xOffset = 0
            for c in line:
                if not c == "\n":
                    position = [(xOffset * 2), 0, (zOffset * 2)]
                    World.ceilingPositions.append(position[0])
                    World.ceilingPositions.append(position[1])
                    World.ceilingPositions.append(position[2])
                    World.ceilingIndices.append(currentCeilingIndex % len(self.ceilingTextures))
                    currentCeilingIndex += 1

                    if c == "*":
                        World.blockPositions.append(position[0])
                        World.blockPositions.append(position[1])
                        World.blockPositions.append(position[2])
                        World.blockIndices.append(currentBlockIndex % len(self.blockTextures))
                        currentBlockIndex += 1
                xOffset += 1
            zOffset += 1

        for zOffset in range(-100, 100):
            for xOffset in range(-100, 100):
                position = [(xOffset * 2), 0, (zOffset * 2)]
                World.floorPositions.append(position[0])
                World.floorPositions.append(position[1])
                World.floorPositions.append(position[2])
                World.floorIndices.append(currentFloorIndex % len(self.floorTextures))
                currentFloorIndex += 1

    def update(self, elapsed):
        self.animateTimer += elapsed
        if self.animateTimer >= self.animateTime:
            self.animateTimer = 0
            for i in range(len(World.blockIndices)):
                World.blockIndices[i] += 1
                World.blockIndices[i] %= len(self.blockTextures)

            World.blockBuffer.setTexIndices(World.blockIndices)

            for i in range(len(World.ceilingIndices)):
                World.ceilingIndices[i] += 1
                World.ceilingIndices[i] %= len(self.ceilingTextures)

            World.ceilingBuffer.setTexIndices(World.ceilingIndices)

            for i in range(len(World.floorIndices)):
                World.floorIndices[i] += 1
                World.floorIndices[i] %= len(self.floorTextures)

            World.floorBuffer.setTexIndices(World.floorIndices)

    def draw(self, shaderManager):
        shaderManager.use()
        shaderManager.setUniform("alphaOffset", 0)
        shaderManager.setUniform("worldMatrix", translation(vec3(0, 0, 0)))

        World.ceilingBuffer.draw(shaderManager)
        World.floorBuffer.draw(shaderManager)
        World.blockBuffer.draw(shaderManager)


