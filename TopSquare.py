from InstancedObject import *

class TopSquare(InstancedObject):
    def __init__(self, tex, texIndices, locations):
        vertexData = array.array("f", [
            -1, 1, -1, -1, 1, 1, 1, 1, 1,
            1, 1, 1, -1, 1, -1, 1, 1, -1
        ])

        textureData = array.array("f", [
            0, 0, 0, 1, 1, 1,
            1, 1, 0, 0, 1, 0
        ])

        normalData = array.array("f", [
            0, -1, 0,
            0, -1, 0,
            0, -1, 0,
            0, -1, 0
        ])

        super().__init__(tex, texIndices, [vertexData, textureData, normalData], locations, 4)

    def draw(self, shaderManager):
        super().draw(shaderManager)
