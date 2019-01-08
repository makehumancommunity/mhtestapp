#version 120

// Declare an attribute (in practice parameter) that can be used
// from the outside to control the behavior of the shader. The
// "somePosition" attribute is a vertex coordinate
attribute vec4 somePosition;

void main() {
  // Simply pass the vertex position to the fragment shader.
  // "gl_Position" is a return value that is piped onwards.
  gl_Position = somePosition;
}

