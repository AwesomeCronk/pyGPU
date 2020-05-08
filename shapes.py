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
