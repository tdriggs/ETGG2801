from Object import *


class InstancedTexturedObject(Object):
    def __init__(self, texArray, data, locations, textureIndicies, dataLengthModifier=1):
        # data indices: [vertex, texture, normal]
        super().__init__(texArray, [data[0], data[1], data[2], array.array("f", [])], dataLengthModifier)

        self.numberInstances = 0
        self.setLocations(locations)

        glBindVertexArray(self.vao)
        self.setArrayBuffer(textureIndicies, len(textureIndicies) * 4)
        self.enableVertexAttribute(ShaderManager.TEXID_INDEX, 1, 1)
        glBindVertexArray(0)

        self.numberTriangles = len(data[0]) // 3

    def setLocations(self, locations):
        glBindVertexArray(self.vao)
        self.setDynamicArrayBuffer(locations, len(locations) * self.dataLengthModifier)
        self.enableVertexAttribute(ShaderManager.OFFSET_INDEX, 3, 1)
        glBindVertexArray(0)
        self.numberInstances = len(locations) // 3

    def setDynamicArrayBuffer(self, data, dataLength):
        glBindBuffer(GL_ARRAY_BUFFER, self.generateBuffer())
        glBufferData(GL_ARRAY_BUFFER, dataLength, data, GL_DYNAMIC_DRAW)

    def draw(self, shaderManager):
        shaderManager.use()
        shaderManager.setUniform("tex", self.texArray)
        glBindVertexArray(self.vao)
        glDrawArraysInstanced(GL_TRIANGLES, 0, self.numberTriangles * 3, self.numberInstances)
