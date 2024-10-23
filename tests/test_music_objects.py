from package.music_objects import Playlist, Song

def test_song():
    song = Song("song", 1)
    assert song.name == "song"
    assert song.id == 1

def test_playlist_init():
    playlist = Playlist("playlist", "playlist_id", [Song("song", 1)])
    assert playlist.name == "playlist"
    assert playlist.id == "playlist_id"
    assert [song.id for song in playlist.get_songs()] == [1]

def test_playlist_add_songs():
    playlist = Playlist("playlist", "playlist_id", [Song("song", 1)])
    playlist.add_songs(Song("new_song", 2))
    playlist.add_songs(Song("new_song", 2)) # do nothing if song already exists
    assert [song.id for song in playlist.get_songs()] == [1, 2]

def test_playlist_remove_songs():
    playlist = Playlist("playlist", "playlist_id", [Song("song", 1), Song("new_song", 2)])
    playlist.remove_songs(Song("song", 1))
    playlist.remove_songs(Song("song", 1)) # do nothing if song doesn't exist``
    assert [song.id for song in playlist.get_songs()] == [2]