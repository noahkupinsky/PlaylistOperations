import pytest
from unittest.mock import patch, MagicMock
from package.music_objects import Playlist, Song
from package.spotify_service import SpotifyService

# Mock data for items to simulate paginated responses
mock_items_page_1 = [{'name': 'Item 1', 'id': 'item_1'}]
mock_items_page_2 = [{'name': 'Item 2', 'id': 'item_2'}]
mock_items_page_3 = [{'name': 'Item 3', 'id': 'item_3'}]

@patch("package.spotify_service.SpotifyOAuth")
@patch("package.spotify_service.spotipy.Spotify")
def test_paginate(mock_spotify, mock_spotify_oauth):
    # Initialize the service
    mock_spotify_instance = mock_spotify.return_value
    mock_spotify_instance.current_user.return_value = {'id': 'mock_user_id'}

    service = SpotifyService()
    
    # Mock initial_call function to simulate paginated API responses
    def mock_getter(limit, offset):
        if offset == 0:
            return {'items': mock_items_page_1, 'total': 3}
        elif offset == 1:
            return {'items': mock_items_page_2, 'total': 3}
        elif offset == 2:
            return {'items': mock_items_page_3, 'total': 3}
        else:
            return {'items': [], 'total': 3}

    # Define a simple item_processor to create Song objects from the mock data
    def item_processor(item):
        return Song(name=item['name'], id=item['id'])

    # Call _paginate directly with limit=1 to force pagination
    result = service._paginate(mock_getter, item_processor, limit=1)
    
    # Assertions
    assert len(result) == 3
    assert result[0].name == 'Item 1'
    assert result[1].name == 'Item 2'
    assert result[2].name == 'Item 3'
    assert isinstance(result[0], Song)
    assert isinstance(result[1], Song)
    assert isinstance(result[2], Song)

# Generate mock data for playlists and songs
mock_playlists_data = [{
    'name': f'Playlist {i+1}', 
    'id': f'playlist_{i+1}', 
    'description': f'Description {i+1}', 
    'owner': {'id': 'mock_user_id'}
    } for i in range(51)]
mock_tracks_data = [{'track': {'name': f'Song {i+1}', 'id': f'song_{i+1}'}} for i in range(51)]

@patch("package.spotify_service.SpotifyOAuth")
@patch("package.spotify_service.spotipy.Spotify")
def test_get_playlists_with_51_playlists_and_51_songs_each(mock_spotify, mock_spotify_oauth):
    # Setup the Spotify instance mock
    mock_spotify_instance = mock_spotify.return_value
    mock_spotify_instance.current_user.return_value = {'id': 'mock_user_id'}

    # Mock paginated response for `current_user_playlists`
    # First call returns the first 50 playlists, next call returns the 51st
    mock_spotify_instance.current_user_playlists.side_effect = [
        {'items': mock_playlists_data[:50], 'total': 51},
        {'items': mock_playlists_data[50:], 'total': 51}
    ]

    # Mock paginated response for `playlist_tracks`
    # First call returns the first 50 songs, next call returns the 51st
    def mock_playlist_tracks(playlist_id, limit, offset):
        if offset == 0:
            return {'items': mock_tracks_data[:50], 'total': 51}
        elif offset == 50:
            return {'items': mock_tracks_data[50:], 'total': 51}
        return {'items': [], 'total': 51}

    # Set the `playlist_tracks` side effect to call our mock function
    mock_spotify_instance.playlist_tracks.side_effect = mock_playlist_tracks

    # Instantiate the SpotifyService object and retrieve playlists
    spotify_service = SpotifyService()
    playlists = spotify_service.get_playlists()  # Using default limit=50

    # Assertions on the number of playlists
    assert len(playlists) == 51
    assert all(isinstance(playlist, Playlist) for playlist in playlists)

    # Assertions on the number of songs in each playlist
    for i, playlist in enumerate(playlists, start=1):
        assert playlist.name == f'Playlist {i}'
        songs = playlist.get_songs()
        assert len(songs) == 51
        assert all(isinstance(song, Song) for song in songs)
        
        # Check the names and IDs of songs in the first playlist as an example
        if i == 1:
            for j, song in enumerate(songs, start=1):
                assert song.name == f'Song {j}'
                assert song.id == f'song_{j}'

    # Verify API call counts
    assert mock_spotify_instance.current_user_playlists.call_count == 2  # Two calls for playlist pagination
    assert mock_spotify_instance.playlist_tracks.call_count == 102  # 51 playlists, each requiring two calls for track pagination