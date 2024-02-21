shader_type canvas_item;

// from https://www.youtube.com/watch?v=nyFzPaWAzeQ
void vertex() {
	if (VERTEX.y < 0.0) {
		VERTEX += vec2(sin(TIME) * 100.0, 0);
	}
}

