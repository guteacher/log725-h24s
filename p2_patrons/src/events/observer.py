from src.events.event import Event


class Observer():
    def __init__(self):
        pass

    def update(self, event):
        if event.score == 1000:
            print("achievement unlocked")
