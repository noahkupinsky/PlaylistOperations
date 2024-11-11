import pytest
from package.playlist_operations import PlaylistOperation, PlaylistOperationAdd, PlaylistOperationRemove
from package.music_objects import Playlist, Song

def create_test_playlist(name, songs):
    return Playlist(name=name, id=name, description=name, songs=songs)

def test_load_playlists():
    playlist_loaders = [create_test_playlist("from", []), create_test_playlist("to", [])]
    operation = PlaylistOperation(*playlist_loaders)
    playlists = operation.load_playlists()
    assert [playlist.name for playlist in playlists] == ["from", "to"]

    invalid_loader = lambda: 15
    operation = PlaylistOperation(invalid_loader)
    with pytest.raises(ValueError):
        operation.load_playlists()

def test_lazy_loading():
    # create dictionary for playlists
    playlists = {}
    playlist_loader = lambda: playlists["key"]

    # create operation without playlists loaded yet
    operation = PlaylistOperation(playlist_loader)

    # add playlists to dictionary
    playlists["key"] = create_test_playlist('test', [Song(name="song", id=1)])

    [playlist] = operation.load_playlists()
    assert [song.id for song in playlist.get_songs()] == [1]

def test_add_operation():
    playlist_from = create_test_playlist('from', [Song(name="song", id=1)])
    playlist_to = create_test_playlist('to', [])
    operation = PlaylistOperationAdd(playlist_from, playlist_to)
    operation.execute()
    assert [song.id for song in playlist_to.get_songs()] == [1]

def test_remove_operation():
    playlist_from = create_test_playlist('from', [Song(name="song", id=1)])
    playlist_to = create_test_playlist('to', [Song(name="song", id=1)])
    operation = PlaylistOperationRemove(playlist_from, playlist_to)
    operation.execute()
    assert [song.id for song in playlist_to.get_songs()] == []

def test_operation_precedence():
    playlist_from = create_test_playlist('from', [Song(name="song", id=1)])
    playlist_to = create_test_playlist('to', [])
    add_operation = PlaylistOperationAdd(playlist_from, playlist_to)
    remove_operation = PlaylistOperationRemove(playlist_from, playlist_to)
    operation_list = [remove_operation, add_operation]
    operation_list.sort()
    assert operation_list == [add_operation, remove_operation]
