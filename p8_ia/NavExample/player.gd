extends CharacterBody2D

const speed = 100
@onready var nav_agent := $NavigationAgent2D as NavigationAgent2D

func _ready() -> void:
	await get_tree().process_frame
	makepath()
	
func _physics_process(_delta: float) -> void:
	var dir = to_local(nav_agent.get_next_path_position()).normalized()
	velocity = dir * speed
	move_and_slide()
	
func makepath():
	nav_agent.target_position = get_global_mouse_position()
	print(nav_agent.target_position)
	
func _on_timer_timeout():
	makepath()
