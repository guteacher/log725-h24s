shader_type canvas_item;

void fragment() {
// Apply a simple blur filter
    vec4 color = vec4(0.0);

    for (float i = -1.0; i <= 1.0; i += 1.0) {
        for (float j = -1.0; j <= 1.0; j += 1.0) {
            color += texture(TEXTURE, SCREEN_UV + vec2(i, j) / 60.0);
        }
    }

    COLOR = color / 9.0;  // Normalize by the number of samples
}
