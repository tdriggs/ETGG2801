from InstancedObject import *

class Billboard(InstancedObject):
    def __init__(self, tex, texIndex, locations):
        vertexData = array.array("f", [
            -1, 1, 0, -1, -1, 0, 1, 1, 0,
            1, 1, 0, -1, -1, 0, 1, -1, 0
        ])

        textureData = array.array("f", [
            0, 0, 0, 1, 1, 0,
            1, 0, 0, 1, 1, 1
        ])

        super().__init__(tex, texIndex, [vertexData, textureData, array.array("f", [])], locations, 4)

    def draw(self, shaderManager, size):
        shaderManager.use()
        shaderManager.setUniform("bbsize", size)
        super().draw(shaderManager)
