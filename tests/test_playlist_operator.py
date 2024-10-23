import pytest
from package.music_objects import Playlist, Song
from package.playlist_operator import PlaylistOperator
from package.playlist_operations import PlaylistOperationAdd, PlaylistOperationRemove

def test_playlist_operator():
    pA = Playlist(name="A [A0]", id="A", songs=[Song("s1", 1), Song("s2", 2), Song("s4", 4)])
    pB = Playlist(name="B [R0]", id="B", songs=[Song("s2", 2)])
    pC = Playlist(name="C [K0]", id="C", songs=[Song("s3", 3)])
    pD = Playlist(name="D [A0]", id="D", songs=[Song("s5", 5), Song("s6", 6)])
    pE = Playlist(name="E [R0]", id="E", songs=[Song("s5", 5), Song("s4", 4)])
    playlists = [pA, pB, pC, pD, pE]
    playlist_operator = PlaylistOperator(playlists)
    playlist_operator.operate()
    songs = [song.id for song in pC.get_songs()]
    songs.sort()
    assert songs == [1, 6]

def test_playlist_operator_errors():
    # prevent multiple key tokens
    with pytest.raises(ValueError):
        pA = Playlist(name="A [K0 K1]", id="A", songs=[Song("s1", 1), Song("s2", 2), Song("s4", 4)])
        playlist_operator = PlaylistOperator([pA])
        playlist_operator.operate()