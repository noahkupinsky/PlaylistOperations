from package.spotify_service import SpotifyService
from package.playlist_operator import PlaylistOperator

if __name__ == "__main__":
    spotify_service = SpotifyService()
    playlists = spotify_service.get_playlists()

    playlist_operator = PlaylistOperator(playlists)
    operated_on = playlist_operator.operate()

    for playlist in operated_on:
        spotify_service.update_playlist(playlist)
    