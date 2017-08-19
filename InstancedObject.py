from Object import *


class InstancedObject(Object):
    def __init__(self, texNames, texIndices, data, locations, dataLengthModifier=1):
        # data indices: [vertex, texture, normal]
        super().__init__(texNames, [data[0], data[1], data[2], array.array("f", [])], dataLengthModifier)

        self.locationBuffer = self.generateBuffer()

        self.numberInstances = 0
        self.setLocations(locations)

        self.textureIndexBuffer = self.generateBuffer()

        self.setTexIndices(texIndices)

        self.numberTriangles = len(data[0]) // 3

    def setLocations(self, locations):
        glBindVertexArray(self.vao)
        self.setDynamicArrayBuffer(array.array("f", locations), len(locations) * self.dataLengthModifier, self.locationBuffer)
        self.enableVertexAttribute(ShaderManager.OFFSET_INDEX, 3, 1)
        glBindVertexArray(0)
        self.numberInstances = len(locations) // 3

    def setTexIndices(self, texIndices):
        glBindVertexArray(self.vao)
        self.setArrayBuffer(array.array("f", texIndices), len(texIndices) * self.dataLengthModifier, self.textureIndexBuffer)
        self.enableVertexAttribute(ShaderManager.TEXINDEX_INDEX, 1, 1)
        glBindVertexArray(0)

    def setDynamicArrayBuffer(self, data, dataLength, buffer):
        glBindBuffer(GL_ARRAY_BUFFER, buffer)
        glBufferData(GL_ARRAY_BUFFER, dataLength, data, GL_DYNAMIC_DRAW)

    def draw(self, shaderManager):
        shaderManager.use()
        shaderManager.setUniform("tex", self.tex)
        glBindVertexArray(self.vao)
        glDrawArraysInstanced(GL_TRIANGLES, 0, self.numberTriangles * 3, self.numberInstances)
        glBindVertexArray(0)
