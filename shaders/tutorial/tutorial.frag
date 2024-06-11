#version 400

in vec2 uvs;
out vec4 f_color;

void main() {
    vec2 uv = uvs;
    vec3 col = vec3(1.0, 0.0, 0.0);
    f_color = vec4(uv.x, 0.0, 0.0, 1.0);
}