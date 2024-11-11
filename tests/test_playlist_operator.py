import pytest
from package.music_objects import Playlist, Song
from package.playlist_operator import PlaylistOperator
from package.playlist_operations import PlaylistOperationAdd, PlaylistOperationRemove

def test_playlist_operator():
    pA = Playlist(name="A", id="A", description="[A0]", songs=[Song("s1", 1), Song("s2", 2), Song("s4", 4)])
    pB = Playlist(name="B", id="B", description=" [R0]", songs=[Song("s2", 2)])
    pC = Playlist(name="C", id="C", description=" [K0]", songs=[Song("s3", 3)])
    pD = Playlist(name="D", id="D", description=" [A0]", songs=[Song("s5", 5), Song("s6", 6)])
    pE = Playlist(name="E", id="E", description=" [R0]", songs=[Song("s5", 5), Song("s4", 4)])
    playlists = [pA, pB, pC, pD, pE]
    playlist_operator = PlaylistOperator(playlists)
    operated_on = playlist_operator.operate()
    songs = [song.id for song in pC.get_songs()]
    songs.sort()
    assert songs == [1, 6]
    assert len(operated_on) == 1
    assert operated_on[0] == pC

def test_playlist_operator_errors():
    # prevent multiple key tokens
    with pytest.raises(ValueError):
        pA = Playlist(name="A", id="A", description="[K0 K1]", songs=[Song("s1", 1), Song("s2", 2), Song("s4", 4)])
        playlist_operator = PlaylistOperator([pA])
        playlist_operator.operate()

def test_playlist_operator_errors():
    # prevent key tokens being found with other tokens
    with pytest.raises(ValueError):
        pA = Playlist(name="A", id="A", description="[K0 A1]", songs=[Song("s1", 1), Song("s2", 2), Song("s4", 4)])
        playlist_operator = PlaylistOperator([pA])
        playlist_operator.operate()