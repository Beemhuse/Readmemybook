class Player:
    def __init__(self):
        self.playing = False

    def play(self):
        self.playing = True

    def pause(self):
        self.playing = False

    def stop(self):
        self.playing = False

    def is_playing(self):
        return self.playing
    # Other methods to control play, pause, etc.
