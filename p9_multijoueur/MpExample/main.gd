extends Node2D
 
var peer = ENetMultiplayerPeer.new()
var hostname = "localhost"
var port = 11234

# la scène qu'on va répliquer
@export var player_scene: PackedScene
 

func _on_host_pressed():
	peer.create_server(port)
	multiplayer.multiplayer_peer = peer
	_add_player()
	multiplayer.peer_connected.connect(_add_player)
	# si un nouveau client connecte, appelez _play_sound
	multiplayer.peer_connected.connect(_play_sound_on_client)

func _add_player(id = 1):
	var player = player_scene.instantiate()
	player.name = str(id)
	call_deferred("add_child", player)
 
func _on_join_pressed():
	peer.create_client(hostname, port)
	multiplayer.multiplayer_peer = peer
 
func _play_sound_on_client(id):
	# appeler _play_sound à distance
	_play_sound.rpc()
	var count = 1
	while(count <= 200):
		_print_some_text.rpc(str(count))
		count += 1
		
@rpc
func _play_sound():
	# jouer le son
	$AudioStreamPlayer.play()
	
	# changer la couleur de l'écran du client seulement
	var pink = Color(1, 0.5, 1, 1)
	$ColorRect.set_color(pink)
	
@rpc("authority", "call_remote", "unreliable")
func _print_some_text(text):
	print(text)
