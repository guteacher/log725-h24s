extends Node2D

func _ready():
	# Create multiple viewports
	for i in range(3):
		var viewport = $SubViewportContainer/SubViewport

		# Set the viewport size
		#viewport.size = Vector2(400, 300)

		# Add a sprite to each viewport
		#var sprite = Sprite2D.new()
		#sprite.texture = preload("res://icon.svg")
		#viewport.add_child(sprite)
		#sprite.position = Vector2(600, 100)

