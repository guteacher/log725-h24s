shader_type canvas_item;

void fragment() {
  if (UV.x > 0.0 && UV.x < 1.0 * sin(TIME)) {
    COLOR = COLOR * vec4(0, 1, 1, 1);
  }
}
