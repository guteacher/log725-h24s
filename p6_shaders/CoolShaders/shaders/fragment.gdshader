shader_type canvas_item;

void fragment() {
    vec4 color = vec4(0.0);

    for (float i = -1.0; i <= 1.0; i += 1.0) {
        for (float j = -1.0; j <= 1.0; j += 1.0) {
            color += vec4(0,0,0,0);
        }
    }

    //COLOR = color / 9.0; 
}
