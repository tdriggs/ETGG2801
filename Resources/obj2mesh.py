import sys
import array
import tkinter.filedialog

if len(sys.argv) == 1:
    infileName = tkinter.filedialog.askopenfilename()
    if not infileName:
        sys.exit(0)
else:
    infileName = sys.argv[1]

dirParts = infileName.split("/")
meshDir = ""
for i in range(0, len(dirParts) - 1):
    meshDir += dirParts[i] + "/"

outfileName = infileName.split(".")[0] + ".mesh"
vertexData = []
normalData = []
textureData = []
triangles = []
materials = {None: {"count": 0}}
workingMaterial = None


infile = open(infileName)
for line in infile:
    line = line.strip()
    if len(line) == 0:
        pass
    elif line.startswith('#'):
        pass
    elif line.startswith("v "):
        tempList = line.split()[1:]
        tempList = [float(q) for q in tempList]
        vertexData.append(tempList)
    elif line.startswith("vn "):
        tempList = line.split()[1:]
        tempList = [float(q) for q in tempList]
        normalData.append(tempList)
    elif line.startswith("vt "):
        tempList = line.split()[1:]
        tempList = [float(q) for q in tempList]
        textureData.append(tempList)
    elif line.startswith("f "):
        tempList = line.split()[1:]
        if len(tempList) != 3:
            print("Non-triangle!")
        else:
            triangle = []
            materials[workingMaterial]["count"] += 1
            for vertex in tempList:
                vertexParts = vertex.split('/')
                if len(vertexParts) == 1:
                    triangle.append((int(vertexParts[0]) - 1, 0, 0))
                elif len(vertexParts) == 2:
                    triangle.append((int(vertexParts[0]) - 1, int(vertexParts[1]) - 1, 0))
                else:
                    if len(vertexParts[1]) == 0:
                        triangle.append((int(vertexParts[0]) - 1, 0, int(vertexParts[2]) - 1))
                    else:
                        triangle.append((int(vertexParts[0]) - 1, int(vertexParts[1]) - 1, int(vertexParts[2]) - 1))
            triangles.append(triangle)
    elif line.startswith("mtllib"):
        materialInfile = open(meshDir + line[7:])
        currentMaterial = None
        for mtlLine in materialInfile:
            mtlLine = mtlLine.strip()
            if len(mtlLine) == 0: pass
            elif mtlLine[0] == '#': pass
            elif mtlLine.startswith("newmtl"):
                currentMaterial = mtlLine[7:]
                materials[currentMaterial] = {"count": 0}
            else:
                tempList = mtlLine.split(" ", 1)
                materials[currentMaterial][str(tempList[0])] = tempList[1]
    elif line.startswith("usemtl"):
        workingMaterial = line[7:]

outTriangleList = []
indexMap = {}
tempList = []
for triangle in triangles:
    for vi, ti, ni in triangle:
        key = (vi, ti, ni)
        if key not in indexMap:
            indexMap[key] = len(tempList)
            tempList.append(key)
        outTriangleList.append(indexMap[key])

outfile = open(outfileName, "wb")
outfile.write(b"mesh_01\n")
outfile.write(("num_verticies " + str(len(tempList)) + "\n").encode())
outfile.write(("num_triangles " + str(len(triangles)) + "\n").encode())

largestCount = 0
largestMaterial = None
for material in materials:
    count = materials[material]["count"]
    if count > largestCount:
        largestCount = count
        largestMaterial = material

outfile.write(("texture_file " + meshDir + materials[largestMaterial]["map_Kd"]).encode())
outfile.write(b"\n")

outVertexList = []
outNormalList = []
outTextureList = []
for vi, ti, ni in tempList:
    outVertexList.append(vertexData[vi][0])
    outVertexList.append(vertexData[vi][1])
    outVertexList.append(vertexData[vi][2])
    outTextureList.append(textureData[ti][0])
    outTextureList.append(textureData[ti][1])
    outNormalList.append(normalData[ni][0])
    outNormalList.append(normalData[ni][1])
    outNormalList.append(normalData[ni][2])

outfile.write(b"verticies\n")
outfile.write(array.array('f', outVertexList).tobytes())
outfile.write(b'\n')

outfile.write(b"normals\n")
outfile.write(array.array('f', outNormalList).tobytes())
outfile.write(b'\n')

outfile.write(b"texcoords\n")
outfile.write(array.array('f', outTextureList).tobytes())
outfile.write(b'\n')

outfile.write(b"indicies\n")
outfile.write(array.array('I', outTriangleList).tobytes())
outfile.write(b'\n')
outfile.write(b'end\n')
print("SUCCESS!")
outfile.close()





