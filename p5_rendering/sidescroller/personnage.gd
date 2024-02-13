extends CharacterBody2D

@export var speed = 400
#@onready var _animated_sprite = $AnimatedSprite2D

func get_input():
	var input_direction = Input.get_vector("left", "right", "up", "down")
	
	# changer vitesse et direction
	velocity = input_direction * speed
	#_animated_sprite.flip_h = input_direction[0] < 0
	
	# si le personnage est déplacé, on joue l'animation
	# print(input_direction)
	#if ():
	#	_animated_sprite.play()
	#else:
	#	_animated_sprite.stop()
	

func _physics_process(delta):
	get_input()
	move_and_slide()
