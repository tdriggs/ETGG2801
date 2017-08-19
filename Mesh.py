from Object import *


class Mesh(Object):
    def __init__(self, fileName):
        infile = open(fileName, "rb")
        line = infile.readline().decode().strip()
        assert line == "mesh_01"

        while line != "end":
            line = infile.readline().decode().strip()
            if line.startswith("num_verticies"):
                tempList = line.split()
                numberVerticies = int(tempList[1])
            elif line.startswith("num_triangles"):
                tempList = line.split()
                numberTriangles = int(tempList[1])
            elif line.startswith("texture_file"):
                texName = [line.split()[1]]
            elif line.startswith("verticies"):
                numberBytes = numberVerticies * 3 * 4
                vertexData = infile.read(numberBytes)
            elif line.startswith("normals"):
                numberBytes = numberVerticies * 3 * 4
                normalData = infile.read(numberBytes)
            elif line.startswith("texcoords"):
                numberBytes = numberVerticies * 2 * 4
                textureData = infile.read(numberBytes)
            elif line.startswith("indicies"):
                numberBytes = numberTriangles * 3 * 4
                indexData = infile.read(numberBytes)

        super().__init__(texName, [vertexData, textureData, normalData, indexData])

    def draw(self, shaderManager):
        super().draw(shaderManager, GL_UNSIGNED_INT)
