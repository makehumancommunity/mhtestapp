#version 120

// This color is fetched from the vertex shader. Note that
// there is a "varying" with the same name there. This causes
// the variables to be connected automatically without us
// having to say so in the python code
varying vec4 outputColor;

void main() {
  // Set the color of all drawn pixels to red
  gl_FragColor = outputColor;
}

