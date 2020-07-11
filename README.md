This is a 3d graphics toolkit for use with PyQt5's QOpenGLWidget. It uses OpenGL and supports custom vertex and fragment shaders.

Currently in the development stage.

---
Object type cheat sheet:

Object: | ID:
---|---
light | 0
triangle |  1
rect. prism |  2
cylinder |  3
sphere |  4
half sphere |  5

### Light:

Values in array: 9

Values: |
---|---
0 | xxx | xxx | x | x | xxx
indicates that this is a light. | Position (xyz) | Orientation (likely Euler) | Light type | light intensity | Light color
int (1) | floats (any value) | floats (0-360) | int (0-4) | float (0-1) | floats (0-1)

### Triangle:

Values in array: 

Values: |
---|---
1 | xxx | xxx | xxx | xxx |
indicates that this is a triangle. | Position of vertex A (xyz) | Position of vertex B (xyz) | Position of vertex C (xyz) | Color
int (1) | floats (any value) | floats (any value) | floats (any value) | floats (0-1)