from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget

from shaderProgram import shader, cube
import sys

def run():
    app = QApplication([])
    window = mainWindow()
    window.show()
    sys.exit(app.exec_())

class mainWindow(QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        self.setGeometry(0, 0, 500, 500)
        self.openGLWidget = QOpenGLWidget(self)
        self.shader = shader(self, self.openGLWidget)
        self.shader.resize(500, 500)
        self.openGLWidget.setGeometry(0, 0, 500, 500)
        self.cube1 = cube((0, 0, 0))
        self.cube2 = cube((1, 0, 0))
        self.cube3 = cube((0, 0, 1))
        self.shader.addShapes(self.cube1, self.cube2, self.cube3)
        self.shader.navigate(vVal = -45)
        self.shader.update()

if __name__ == '__main__':
    run()