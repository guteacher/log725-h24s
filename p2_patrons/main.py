from climber_game import ClimberGame
from src.events.observer import Observer

cg = ClimberGame()

obs = Observer()
cg.attach(obs)

# faire l'initialization
cg.main()

# démarre la première scène, le menu
cg.main_menu()
