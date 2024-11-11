from package.spotify_service import SpotifyService
from package.playlist_operator import PlaylistOperator
import logging
from datetime import datetime

# Set up logging to write to a file named `app.log`
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    try:
        spotify_service = SpotifyService()
        playlists = spotify_service.get_playlists()

        playlist_operator = PlaylistOperator(playlists)
        operated_on = playlist_operator.operate()

        for playlist in operated_on:
            spotify_service.update_playlist(playlist)

        logging.info(f"Successfully updated {len(operated_on)} playlists.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
    