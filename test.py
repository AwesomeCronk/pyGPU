from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget

from shaderProgram import shaderManager
from shaderProgram import shader as _shader
#from shapes import cube
import sys

def run(mode):
    app = QApplication([])
    window = mainWindow(mode)
    window.show()
    sys.exit(app.exec_())

class mainWindow(QMainWindow):
    def __init__(self, mode):
        super(mainWindow, self).__init__()
        self.setGeometry(0, 0, 500, 500)
        self.openGLWidget = QOpenGLWidget(self)
        self.openGLWidget.setGeometry(0, 0, 500, 500)
        if mode == 'unsafe':
            self.shader = _shader(self, self.openGLWidget)
            self.shader.resize(500, 500)
            #self.cube1 = cube((0, 0, 0))
            #self.cube2 = cube((1, 0, 0))
            #self.cube3 = cube((0, 0, 1))
            #self.shader.addShapes(self.cube1, self.cube2, self.cube3)
            #self.shader.navigate(vVal = -45)
            #self.shader.update()
        else:
            with shaderManager(self, self.openGLWidget) as shader:
                self.shader = shader
                self.shader.resize(500, 500)
                #self.cube1 = cube((0, 0, 0))
                #self.cube2 = cube((1, 0, 0))
                #self.cube3 = cube((0, 0, 1))
                #self.shader.addShapes(self.cube1, self.cube2, self.cube3)
                #self.shader.navigate(vVal = -45)
                #self.shader.update()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        run(sys.argv[1])
    else:
        run('normal')