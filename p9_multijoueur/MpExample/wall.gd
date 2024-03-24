extends Area2D

var speed = 10
var is_collided = false

func _on_body_entered(body):
	is_collided = true
	
func _process(delta):
	if is_collided:
		rotation+=speed*delta
