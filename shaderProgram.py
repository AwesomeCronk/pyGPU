from OpenGL.GL import (
                       shaders, GL_VERTEX_SHADER, GL_FRAGMENT_SHADER,
                       glLoadIdentity, glTranslatef, glRotatef,
                       glBegin, glEnd, glClear, glVertex3fv,
                       GL_LINES, GL_QUADS, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT
                      )
from OpenGL.GLU import gluPerspective
from exceptions import *

class shader():
    #context data
    context = None
    sizeX = 100
    sizeY = 100

    #drawing data
    rotateDegreeV = 0
    rotateDegreeH = 0
    zoomLevel = -5
    vOffset = -90

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

    def __init__(self, parent, context):
        self.context = context
        self.context.initializeGL = self.initGL
        self.context.paintGL = self.paintGL

    def addShape(self, newShape):
        #for s in self.legalShapes:
         #   if not type(newShape) is s:
          #      raise invalidShapeError("Shape {} is not valid.".format(s))
           #     return
        self.shapes.append(newShape)

    def update(self):
        self.context.update()
    
    def resize(self, x, y):
        self.sizeX = x
        self.sizeY = y
        self.context.resizeGL(self.sizeX, self.sizeY)

    def navigate(self, hVal, vVal, zVal):
        self.rotateDegreeH += hVal
        self.rotateDegreeV += vVal
        self.zoomLevel += zVal

    def initGL(self):
        self.vertProg = open(self.vertPath, 'r')
        self.fragProg = open(self.fragPath, 'r')
        self.vertCode = self.vertProg.read()
        self.fragCode = self.fragProg.read()
        self.vertShader = shaders.compileShader(self.vertCode, GL_VERTEX_SHADER)
        self.fragShader = shaders.compileShader(self.fragCode, GL_FRAGMENT_SHADER)
        self.shader = shaders.compileProgram(self.vertShader, self.fragShader)
        
    def paintGL(self):
        #This function uses shape objects, such as cube() or mesh(). Shape objects require the following:
        #a list named 'vertices' - This list is a list of points, from which edges and faces are drawn.
        #a list named 'wires'    - This list is a list of tuples which refer to vertices, dictating where to draw wires.
        #a list named 'facets'   - This list is a list of tuples which refer to vertices, ditating where to draw facets.
        #a bool named 'render'   - This bool is used to dictate whether or not to draw the shape.
        #a bool named 'drawWires' - This bool is used to dictate whether wires should be drawn.
        #a bool named 'drawFaces' - This bool is used to dictate whether facets should be drawn.
        
        shaders.glUseProgram(self.shader)
        glLoadIdentity()
        gluPerspective(45, self.sizeX / self.sizeY, 0.1, 110.0)    #set perspective?
        glTranslatef(0, 0, self.zoomLevel)    #I used -10 instead of -2 in the PyGame version.
        glRotatef(self.rotateDegreeV + self.vOffset, 1, 0, 0)    #I used 2 instead of 1 in the PyGame version.
        glRotatef(self.rotateDegreeH, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        for s in self.shapes:
            glBegin(GL_LINES)
            for w in s.wires:
                for v in w:
                    glVertex3fv(s.vertices[v])
            glEnd()
        
            glBegin(GL_QUADS)
            
            for f in s.facets:
                for v in f:
                    glVertex3fv(s.vertices[v])
            glEnd()

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