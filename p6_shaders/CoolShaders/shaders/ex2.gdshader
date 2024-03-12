shader_type canvas_item;

uniform float freq = 50.0;
uniform float amp = 0.0;

void vertex() {
    if (UV.x > 0.5) {
        vec2 distortion = vec2(
            cos((TIME * freq) + VERTEX.x),
            sin((TIME * freq) + VERTEX.y)
        ) * amp;
        VERTEX += distortion;
    }

}