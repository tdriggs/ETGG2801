from math3d import *


class Camera:
    def __init__(self, initialPos, initialLook, **kw):
        self.fov_h = kw.get("fov", 45)
        self.hither = kw.get("hither", 0.1)
        self.yon = kw.get("yon", 1000)
        self.aspect_ratio = kw.get("aspect_ratio", 1)
        self.fov_v = 1.0 / self.aspect_ratio * self.fov_h
        self.eye = initialPos
        self.U = vec3(0, 0, 0)
        self.V = vec3(0, 0, 0)
        self.W = vec3(0, 0, 0)
        self.lookAt(self.eye, initialLook, vec3(0, 1, 0))
        self.compute_proj_matrix()
        self.compute_view_matrix()

    def move(self, amountX, amountY, amountZ):
        self.eye *= translation(amountX * self.U)
        self.eye *= translation(amountY * self.V)
        self.eye *= translation(-amountZ * self.W)
        self.compute_view_matrix()

    def turn(self, angle):
        m = axisRotation(self.V, angle)
        self.U *= m
        self.W *= m
        self.compute_view_matrix()

    def compute_proj_matrix(self):
        self.projmatrix = mat4(
            1 / math.tan(math.radians(self.fov_h)), 0, 0, 0,
            0, 1 / math.tan(math.radians(self.fov_v)), 0, 0,
            0, 0, 1 + 2 * self.yon / (self.hither - self.yon), -1,
            0, 0, 2 * self.hither * self.yon / (self.hither - self.yon), 0)

    def compute_view_matrix(self):
        self.viewmatrix = mat4(1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, -self.eye.x, -self.eye.y, -self.eye.z, 1) * mat4(
            self.U.x, self.V.x, self.W.x, 0, self.U.y, self.V.y, self.W.y, 0, self.U.z, self.V.z, self.W.z, 0, 0, 0, 0,
            1)

    def lookAt(self, eye, coi, up):
        self.eye = vec4(eye.xyz, 1)
        look = normalize(vec4(coi.xyz, 1) - vec4(eye.xyz, 1))
        up = vec4(up.xyz, 0)
        self.W = -look
        self.U = cross(look, up)
        self.V = cross(self.U, look)
        self.compute_view_matrix()

    def draw(self, shaderManager, billboardShaderManager):
        shaderManager.use()
        shaderManager.setUniform("eyePosition", self.eye.xyz)
        shaderManager.setUniform("viewMatrix", self.viewmatrix)
        shaderManager.setUniform("projMatrix", self.projmatrix)

        billboardShaderManager.use()
        billboardShaderManager.setUniform("viewMatrix", self.viewmatrix)
        billboardShaderManager.setUniform("projMatrix", self.projmatrix)
