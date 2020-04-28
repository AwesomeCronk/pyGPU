from OpenGL.GL import (
                       shaders, GL_VERTEX_SHADER, GL_FRAGMENT_SHADER, glUseProgram,
                       glLoadIdentity, glTranslatef, glRotatef,
                       glBegin, glEnd, glClear, glVertex3fv,
                       GL_LINES, GL_QUADS, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_FLOAT, GL_TRIANGLES, glEnableVertexAttribArray, glDrawArrays,
                       glGenVertexArrays, glBindVertexArray, glGenBuffers, glBindBuffer,
                       GL_ARRAY_BUFFER, GLfloat, glBufferData, GL_STATIC_DRAW, glVertexAttribPointer
                      )
from OpenGL.GLU import gluPerspective
from exceptions import *
import ctypes

class shaderManager():          #context manager to ensure resource cleanup
    def __init__(self, parent, viewPort):
        self.parent = parent
        self.viewPort = viewPort
    def __enter__(self):
        self.shader = shader(self.parent, self.viewPort)
        return self.shader
    def __exit__(self):
        self.shader.crashCleanup()

class shader():
    #viewPort data
    parent = None
    viewPort = None
    sizeX = 100
    sizeY = 100

    #drawing data
    rotateDegreeV = 0
    rotateDegreeH = 0
    zoomLevel = -5
    vOffset = 0

    shapes = []
    #legalShapes = [cube]
    
    #shader data
    vertPath = 'vertexShader.glsl'
    fragPath = 'fragmentShader.glsl'
    vertProg = None
    fragProg = None
    vertCode = ''
    fragCode = ''
    vertShader = None
    fragShader = None

    #crash data
    crashFlag = False

    def __init__(self, parent, viewPort):
        self.parent = parent
        self.viewPort = viewPort
        self.viewPort.initializeGL = self.initGL
        self.viewPort.paintGL = self.paintGL

    def addShapes(self, *newShapes):
        for newShape in newShapes:
            #for s in self.legalShapes:
             #   if not type(newShape) is s:
              #      raise invalidShapeError("Shape {} is not valid.".format(s))
               #     return
            self.shapes.append(newShape)

    def update(self):
        self.viewPort.update()
    
    def resize(self, x, y):
        self.sizeX = x
        self.sizeY = y
        self.viewPort.resizeGL(self.sizeX, self.sizeY)

    def navigate(self, hVal = 0, vVal = 0, zVal = 0):
        self.rotateDegreeH += hVal
        self.rotateDegreeV += vVal
        self.zoomLevel += zVal

    def initGL(self):
        self.vertexData = [
                           -1, -1, 0,
                           1, -1, 0,
                           0, 1, 0
                          ]

        self.vertexArrayID = glGenVertexArrays(1)
        glBindVertexArray(self.vertexArrayID)

        self.attrID = 0
        self.vertexBuffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertexBuffer)
        arrayType = GLfloat * len(self.vertexData)
        glBufferData(GL_ARRAY_BUFFER,
                     len(self.vertexData) * ctypes.sizeof(ctypes.c_float),
                     arrayType(*self.vertexData),
                     GL_STATIC_DRAW)
        glVertexAttribPointer(self.attrID, 3, GL_FLOAT, False, 0, None)
        glEnableVertexAttribArray(self.attrID)
        
        #access the code for the vertex and fragment shaders
        self.vertProg = open(self.vertPath, 'r')
        self.fragProg = open(self.fragPath, 'r')
        self.vertCode = self.vertProg.read()
        self.fragCode = self.fragProg.read()
        self.vertProg.close()
        self.fragProg.close()
        #compile those shaders
        self.vertShader = shaders.compileShader(self.vertCode, GL_VERTEX_SHADER)
        self.fragShader = shaders.compileShader(self.fragCode, GL_FRAGMENT_SHADER)
        self.shader = shaders.compileProgram(self.vertShader, self.fragShader)
        
#paintGL uses shape objects, such as cube() or mesh(). Shape objects require the following:
#a list named 'vertices' - This list is a list of points, from which edges and faces are drawn.
#a list named 'wires'    - This list is a list of tuples which refer to vertices, dictating where to draw wires.
#a list named 'facets'   - This list is a list of tuples which refer to vertices, ditating where to draw facets.
#a bool named 'render'   - This bool is used to dictate whether or not to draw the shape.
#a bool named 'drawWires' - This bool is used to dictate whether wires should be drawn.
#a bool named 'drawFaces' - This bool is used to dictate whether facets should be drawn.

    def paintGL(self):
        if self.crashFlag:      #run cleanup operations
            glDisableVertexAttribArray(self.attrID)
            glDeleteBuffers(1,[self.vertexBuffer])
            glDeleteVertexArrays(1, [self.vertexArrayID])
        glUseProgram(self.shader)
        glLoadIdentity()
        gluPerspective(45, self.sizeX / self.sizeY, 0.1, 110.0)    #set perspective
        glTranslatef(0, 0, self.zoomLevel)
        glRotatef(self.rotateDegreeV + self.vOffset, 1, 0, 0)
        glRotatef(self.rotateDegreeH, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        
        #for s in self.shapes:
         #   if s.drawWires:
          #      glBegin(GL_LINES)
           #     for w in s.wires:
            #        for v in w:
             #           glVertex3fv(s.vertices[v])
              #  glEnd()

           # if s.drawFaces:
            #    glBegin(GL_QUADS)
             #   for f in s.facets:
              #      for v in f:
               #         glVertex3fv(s.vertices[v])
                #glEnd()

    def crashCleanup(self):
        self.crashFlag = True
        self.viewPort.update()

class cube():
    render = True
    def __init__(self, location = (0, 0, 0), size = 0.1, drawWires = True, drawFaces = False, color = (1, 1, 1)):
        self.location = location
        self.size = size
        self.drawWires = drawWires
        self.drawFaces = drawFaces
        self.color = color
        self.compute()

    def compute(self):
        x, y, z = self.location
        s = self.size / 2
        self.vertices = [    #8 corner points calculated in reference to the supplied center point
                         (-s + x, s + y, -s + z), (s + x, s + y, -s + z),
                         (s + x, -s + y, -s + z), (-s + x, -s + y, -s + z),
                         (-s + x, s + y, s + z), (s + x, s + y, s + z),
                         (s + x, -s + y, s + z), (-s + x, -s + y, s + z)
                        ]
        self.wires = [    #12 tuples referencing the corner points
                      (0,1), (0,3), (0,4), (2,1), (2,3), (2,6),
                      (7,3), (7,4), (7,6), (5,1), (5,4), (5,6)
                     ]
        self.facets = [    #6 tuples referencing the corner points
                       (0, 1, 2, 3), (0, 1, 6, 5), (0, 3, 7, 4),
                       (6, 5, 1, 2), (6, 7, 4, 5), (6, 7, 3, 2)
                      ]
    def show(self):
        self.render = True
    def hide(self):
        self.render = False
    def move(self, location):
        self.location = location
        self.compute()
    def recolor(self, col):
        if type(col) is tuple:
            self.color = col