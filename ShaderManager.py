import math3d
from Texture import *
from glconstants import *
from glfuncs import *


class ShaderManager:
    POSITION_INDEX = 0
    COLOR_INDEX = 1
    TEXCOORD_INDEX = 2
    NORMAL_INDEX = 3
    OFFSET_INDEX = 4
    TEXINDEX_INDEX = 5

    class FloatSetter:
        def __init__(self, name, loc):
            self.name = name
            self.loc = loc

        def set(self, value):
            v = float(value)
            glUniform1f(self.loc, v)

    class Sampler2dSetter:
        def __init__(self, name, loc, unit):
            self.name = name
            self.loc = loc
            self.unit = unit

        def set(self, value):
            if not isinstance(value, Texture2D):
                raise RuntimeError("Not the correct type")
            value.bind(self.unit)
            glUniform1i(self.loc, self.unit)

    class Sampler2dArraySetter:
        def __init__(self, name, loc, unit):
            self.name = name
            self.loc = loc
            self.unit = unit

        def set(self, value):
            if not isinstance(value, ImageTextureArray):
                raise RuntimeError("Not the correct type")
            value.bind(self.unit)
            glUniform1i(self.loc, self.unit)

    class Vec2Setter:
        def __init__(self, name, loc):
            self.name = name
            self.loc = loc

        def set(self, v):
            if type(v) != math3d.vec2:
                raise RuntimeError("Not the correct type")
            glUniform2f(self.loc, v.x, v.y)

    class Vec3Setter:
        def __init__(self, name, loc):
            self.name = name
            self.loc = loc

        def set(self, v):
            if type(v) != math3d.vec3:
                raise RuntimeError("Not the correct type")
            glUniform3f(self.loc, v.x, v.y, v.z)

    class Vec3ArraySetter:
        def __init__(self, name, loc, size):
            self.name = name
            self.loc = loc
            self.size = size

        def set(self, v):
            if type(v) != list:
                raise RuntimeError("Not the correct type")
            if len(v) != self.size:
                raise RuntimeError("Not the correct size")
            tmp = []
            for i in range(self.size):
                tmp.append(v[i].x)
                tmp.append(v[i].y)
                tmp.append(v[i].z)
            tmp = array.array('f', tmp)
            glUniform3fv(self.loc, self.size, tmp)

    class Mat4Setter:
        def __init__(self, name, loc):
            self.name = name
            self.loc = loc

        def set(self, v):
            if type(v) != math3d.mat4:
                raise RuntimeError("Not the correct type")
            glUniformMatrix4fv(self.loc, 1, True, v.tobytes())

    def __init__(self, vertexShaderName, fragmentShaderName):
        tempList = array.array("I", [0])

        vertexShader = self.makeShader(vertexShaderName, GL_VERTEX_SHADER)
        fragmentShader = self.makeShader(fragmentShaderName, GL_FRAGMENT_SHADER)
        self.shaderManager = glCreateProgram()
        glAttachShader(self.shaderManager, vertexShader)
        glAttachShader(self.shaderManager, fragmentShader)

        glBindAttribLocation(self.shaderManager, ShaderManager.POSITION_INDEX, "a_position")
        glBindAttribLocation(self.shaderManager, ShaderManager.COLOR_INDEX, "a_color")
        glBindAttribLocation(self.shaderManager, ShaderManager.TEXCOORD_INDEX, "a_texcoord")
        glBindAttribLocation(self.shaderManager, ShaderManager.NORMAL_INDEX, "a_normal")
        glBindAttribLocation(self.shaderManager, ShaderManager.OFFSET_INDEX, "a_offset")
        glBindAttribLocation(self.shaderManager, ShaderManager.TEXINDEX_INDEX, "a_texIndex")

        glLinkProgram(self.shaderManager)
        log = bytearray(4096)
        glGetProgramInfoLog(self.shaderManager, len(log), tempList, log)
        if tempList[0] > 0:
            log = log[:tempList[0]].decode()
            print("Linking", vertexShaderName, "+", fragmentShaderName, ":")
            print(log)
        glGetProgramiv(self.shaderManager, GL_LINK_STATUS, tempList)
        if not tempList[0]:
            raise RuntimeError("Could not link shaders.")

        self.uniforms = {}
        textureCount = 0
        glGetProgramiv(self.shaderManager, GL_ACTIVE_UNIFORMS, tempList)
        numberUniforms = tempList[0]
        for i in range(numberUniforms):
            type_ = array.array("I", [0])
            size = array.array("I", [0])
            index = array.array("I", [0])
            name = array.array("B", [0] * 256)
            le = array.array("I", [0])

            tempList[0] = i

            glGetActiveUniformsiv(self.shaderManager, 1, tempList, GL_UNIFORM_TYPE, type_)
            glGetActiveUniformsiv(self.shaderManager, 1, tempList, GL_UNIFORM_SIZE, size)
            glGetActiveUniformName(self.shaderManager, i, len(name), le, name)
            name = name[:le[0]].tobytes().decode()
            loc = glGetUniformLocation(self.shaderManager, name)

            if type_[0] == GL_FLOAT and size[0] == 1:
                setter = ShaderManager.FloatSetter(name, loc)
            elif type_[0] == GL_FLOAT_VEC2 and size[0] == 1:
                setter = ShaderManager.Vec2Setter(name, loc)
            elif type_[0] == GL_FLOAT_VEC3 and size[0] == 1:
                setter = ShaderManager.Vec3Setter(name, loc)
            elif type_[0] == GL_FLOAT_VEC3 and size[0] > 1:
                setter = ShaderManager.Vec3ArraySetter(name, loc, size[0])
            elif type_[0] == GL_FLOAT_MAT4 and size[0] == 1:
                setter = ShaderManager.Mat4Setter(name, loc)
            elif type_[0] == GL_SAMPLER_2D and size[0] == 1:
                setter = ShaderManager.Sampler2dSetter(name, loc, textureCount)
                textureCount += 1
            elif type_[0] == GL_SAMPLER_2D_ARRAY and size[0] == 1:
                setter = ShaderManager.Sampler2dArraySetter(name, loc, textureCount)
                textureCount += 1
            else:
                raise RuntimeError("Don't know about type of " + name)

            self.uniforms[name] = setter

    def setUniform(self, name, value):
        if ShaderManager.active != self:
            raise RuntimeError("Cannot set uniform on non-active program")
        if name in self.uniforms:
            self.uniforms[name].set(value)
        else:
            print("No such uniform", name)

    def use(self):
        glUseProgram(self.shaderManager)
        ShaderManager.active = self

    def makeShader(self, fileName, shaderType):
        shaderData = open(fileName).read()
        shader = glCreateShader(shaderType)
        glShaderSource(shader, 1, [shaderData], None)
        glCompileShader(shader)
        log = bytearray(4096)
        tmp = array.array("I", [0])
        glGetShaderInfoLog(shader, len(log), tmp, log)
        if tmp[0] > 0:
            log = log[:tmp[0]].decode()
            print("When compiling", shaderType, fileName, ":")
            print(log)
        glGetShaderiv(shader, GL_COMPILE_STATUS, tmp)
        if not tmp[0]:
            raise RuntimeError("Cannot compile " + fileName)
        return shader
