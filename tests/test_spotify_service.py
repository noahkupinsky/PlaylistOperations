import pytest
from unittest.mock import patch, MagicMock
from package.spotify_service import SpotifyService

@patch("package.spotify_service.spotipy.Spotify")
def test_get_playlists(mock_spotify):
    # Mock user profile response
    mock_spotify_instance = mock_spotify.return_value
    mock_spotify_instance.current_user.return_value = {'id': 'mock_user_id'}

    # Mock paginated playlist response
    mock_spotify_instance.current_user_playlists.return_value = {
        'items': [
            {'name': 'Playlist 1', 'owner': {'id': 'mock_user_id'}},
            {'name': 'Playlist 2', 'owner': {'id': 'mock_user_id'}},
            {'name': 'Followed Playlist', 'owner': {'id': 'another_user'}}
        ],
        'next': 'next_page_url'
    }
    # Mock the `next` method to return the second page with 'next': None
    mock_spotify_instance.next.side_effect = [
        {'items': [{'name': 'Playlist 3', 'owner': {'id': 'mock_user_id'}}], 'next': None}
    ]
    # Instantiate class and call get_playlists
    spotify_service = SpotifyService()
    playlists = spotify_service.get_playlists()

    # Check results
    assert len(playlists) == 3
    assert playlists[0]['name'] == 'Playlist 1'
    assert playlists[1]['name'] == 'Playlist 2'
    assert playlists[2]['name'] == 'Playlist 3'
    assert all(playlist['owner']['id'] == 'mock_user_id' for playlist in playlists)

    # Verify calls
    mock_spotify_instance.current_user.assert_called_once()
    mock_spotify_instance.current_user_playlists.assert_called_once()
    assert mock_spotify_instance.next.call_count == 1