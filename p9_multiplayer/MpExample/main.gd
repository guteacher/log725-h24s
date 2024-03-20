extends Node2D
 
var peer = ENetMultiplayerPeer.new()
var hostname = "localhost"
var port = 135

# la scène qu'on va répliquer
@export var player_scene: PackedScene
 
 
func _on_host_pressed():
	peer.create_server(port)
	# ajouter un pair
	# on va créer un nouveau joueur (le host)
	# si un client connecte, on va créer un autre joueur (le client)

 
func _add_player(id = 1):
	var player = player_scene.instantiate()
	player.name = str(id)
	# ajouter à l'arbre (des noeuds dans la scène)
 
 
func _on_join_pressed():
	peer.create_client(hostname, port)
	# ajouter un pair
 
