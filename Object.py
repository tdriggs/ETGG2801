from glconstants import *
from glfuncs import *
import array
from ShaderManager import *
import math


class Object:
    def __init__(self, texNames, data, dataLengthModifier=1):
        # data indices: [vertex, texture, normal, index]
        self.tex = ImageTextureArray(texNames)
        self.dataLengthModifier = dataLengthModifier

        self.numberTriangles = len(data[3])

        bufferList = array.array("I", [0])
        glGenVertexArrays(1, bufferList)
        self.vao = bufferList[0]

        glBindVertexArray(self.vao)

        self.vertexBuffer = self.generateBuffer()
        self.setArrayBuffer(data[0], len(data[0]) * self.dataLengthModifier, self.vertexBuffer)
        self.enableVertexAttribute(ShaderManager.POSITION_INDEX, 3)

        self.textureCoordBuffer = self.generateBuffer()
        self.setArrayBuffer(data[1], len(data[1]) * self.dataLengthModifier, self.textureCoordBuffer)
        self.enableVertexAttribute(ShaderManager.TEXCOORD_INDEX, 2)

        self.normalBuffer = self.generateBuffer()
        self.setArrayBuffer(data[2], len(data[2]) * self.dataLengthModifier, self.normalBuffer)
        self.enableVertexAttribute(ShaderManager.NORMAL_INDEX, 3)

        self.indexBuffer = self.generateBuffer()
        self.setElementArrayBuffer(data[3], len(data[3]) * math.ceil(self.dataLengthModifier / 2), self.indexBuffer)

        glBindVertexArray(0)

    def generateBuffer(self):
        bufferList = array.array("I", [0])
        glGenBuffers(1, bufferList)
        return bufferList[0]

    def setArrayBuffer(self, data, dataLength, buffer):
        glBindBuffer(GL_ARRAY_BUFFER, buffer)
        glBufferData(GL_ARRAY_BUFFER, dataLength, data, GL_STATIC_DRAW)

    def setElementArrayBuffer(self, data, dataLength, buffer):
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, dataLength, data, GL_STATIC_DRAW)

    def enableVertexAttribute(self, shaderIndex, numberDataPoints, instanced=0):
        glEnableVertexAttribArray(shaderIndex)
        glVertexAttribPointer(shaderIndex, numberDataPoints, GL_FLOAT, False, numberDataPoints * 4, 0)
        glVertexAttribDivisor(shaderIndex, instanced)

    def draw(self, shaderManager, type):
        shaderManager.use()
        shaderManager.setUniform("tex", self.tex)
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, self.numberTriangles * 3, type, 0)
        glBindVertexArray(0)
