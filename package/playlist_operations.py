from typing import TypeAlias
from collections.abc import Callable
from package.music_objects import Playlist

PlaylistLoader: TypeAlias = Callable[[], Playlist]

class PlaylistOperation:
    precedence = -1

    def __init__(self, *playlist_loaders: list[PlaylistLoader]):
        self.playlist_loaders = playlist_loaders

    def execute(self):
        pass

    def load_playlists(self):
        playlists = [loader() for loader in self.playlist_loaders]
        if not all(isinstance(playlist, Playlist) for playlist in playlists):
            raise ValueError("All playlist loaders must return a playlist")
        return playlists

    def __lt__(self, other):
        if not isinstance(other, PlaylistOperation):
            return NotImplemented
        return self.precedence < other.precedence
    
class PlaylistOperationAdd(PlaylistOperation):
    precedence = 0

    def execute(self):
        from_playlist, to_playlist = self.load_playlists()
        songs_to_add = from_playlist.get_songs()
        to_playlist.add(*songs_to_add)

class PlaylistOperationRemove(PlaylistOperation):
    precedence = 1

    def execute(self):
        from_playlist, to_playlist = self.load_playlists()
        songs_to_remove = from_playlist.get_songs()
        to_playlist.remove(*songs_to_remove)
