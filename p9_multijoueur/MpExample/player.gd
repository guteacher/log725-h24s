extends CharacterBody2D
 
func _enter_tree():
	var id = name.to_int()
	set_multiplayer_authority(id)
	
	if (id == 1):
		position.x = 100
		position.y = 0
	else:
		position.x = 100
		position.y = 100
 
func _physics_process(delta):
	# définir authorité sur l'objet
	if is_multiplayer_authority():
		velocity = Input.get_vector("ui_left","ui_right","ui_up","ui_down") * 400
	move_and_slide()
