from package.spotify_service import SpotifyService

if __name__ == "__main__":
    spotify_service = SpotifyService()
    playlists = spotify_service.get_playlists()
    absolute_jams = [playlist for playlist in playlists if playlist.name == "Absolute Jams"][0]
    songs = absolute_jams.get_songs()
    print(len(songs))
    for song in songs:
        print(str(song))