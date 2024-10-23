class Song:
    def __init__(self, name: str, id: any):
        self.name = name
        self.id = id

class Playlist:
    def __init__(self, name: str, id: any, songs: list[Song]):
        self.name = name
        self.id = id
        self.songs = {song.id: song for song in songs}

    def add(self, *songs: list[Song]):
        for song in songs:
            self.songs[song.id] = song

    def remove(self, *songs: list[Song]):
        for song in songs:
            self.songs.pop(song.id, None) # remove song if it exists, do nothing if it doesn't

    def clear(self):
        self.songs = {}

    def get_songs(self) -> list[Song]:
        return list(self.songs.values())
    
    def __call__(self, *args, **kwds):
        return self