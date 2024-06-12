#version 400

in vec2 fragCoord;
out vec4 fragColor;

uniform vec2 iResolution;
uniform float iTime;

const float PI = 3.1415926535897932384626433832795;
const vec2 HALF = vec2(0.5);
const float rotSpeed = 8.;


float deg2rad(float deg) {
    return deg * PI / 180.0;
}

vec3 palette(float t) {
    vec3 a = vec3(0.5, 0.5, 0.5);
    vec3 b = vec3(0.5, 0.5, 0.5);
    vec3 c = vec3(1.0, 1.0, 1.0);
    vec3 d = vec3(0.263, 0.416, 0.557);
    return a + b*cos(6.28318*(c*t+d));
}

void main()
{
    vec2 uv = (fragCoord*2.0) - iResolution.xy / iResolution.y;
    float sin_factor = sin(deg2rad(iTime*rotSpeed + sin(iTime)));
    float cos_factor = cos(deg2rad(iTime*rotSpeed) + 1.4*sin(iTime));

    uv *= mat2(cos_factor, sin_factor, -sin_factor, cos_factor);
    uv *= vec2(iResolution.y / iResolution.x, iResolution.x / iResolution.y);

    vec2 uv0 = uv;
    vec3 finalColor = vec3(0.0);
    
    for (float i = 0.0; i < 4.0; i++) {
        uv = fract(uv * 1.5) - 0.5;
    
        float d = length(uv) * exp(-length(uv0));
        vec3 col = palette(length(uv0) + i*.4 + iTime*.4);
        d = sin(d*8. + iTime)/8.;
        d = abs(d);
        
        d = pow(0.01 / d, 1.2);
        finalColor += col * d;
    }
    
    
    fragColor = vec4(finalColor, 1.0);
}