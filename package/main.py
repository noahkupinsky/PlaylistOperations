from spotify_service import SpotifyService

if __name__ == "__main__":
    spotify_service = SpotifyService()
    user_playlists = spotify_service.get_playlists()
    for playlist in user_playlists:
        print(playlist['name'], playlist['id'])