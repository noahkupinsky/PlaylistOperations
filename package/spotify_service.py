from package.music_objects import Playlist, Song
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth, CacheFileHandler

# Load environment variables from .env file
load_dotenv()

class SpotifyService:
    def __init__(self):
        self.sp = self._create_spotify_instance()
        self.user_id = self._get_user_id()

    def _create_spotify_instance(self):
        cache_handler = CacheFileHandler(cache_path="../.cache")  # Adjust this path as needed

        return spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIFY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
            scope="playlist-modify-public playlist-modify-private playlist-read-private",
            cache_handler=cache_handler  # Path to cache file
        ))
    
    def _is_owned_by_user(self, playlist):
        return playlist.get('owner', {}).get('id') == self.user_id

    def _get_user_id(self):
        user_profile = self.sp.current_user()
        return user_profile['id']
    
    def _paginate(self, getter, item_processor, limit=50):
        offset = 0
        items = []

        # Make the initial call to get the total count
        results = getter(limit=limit, offset=offset)
        total = results.get('total', 0)

        while offset < total:
            # Process each item in the current page
            for item in results['items']:
                processed_item = item_processor(item)
                if processed_item:
                    items.append(processed_item)

            # Update offset to fetch the next page
            offset += limit

            # Fetch the next page if we haven’t reached the total count
            if offset < total:
                results = getter(limit=limit, offset=offset)

        return items
    
    def get_playlists(self):
        def process_playlist_item(playlist_data):
            # Only process if the playlist is owned by the user
            if self._is_owned_by_user(playlist_data):
                songs = self._get_songs_for_playlist(playlist_data['id'])
                return Playlist(
                    name=playlist_data['name'], 
                    id=playlist_data['id'], 
                    description=playlist_data['description'],
                    songs=songs
                    )
            return None  # Skip if not owned by user

        # Use the paginator HOF to fetch and process all user playlists
        return self._paginate(self.sp.current_user_playlists, process_playlist_item)

    def _get_songs_for_playlist(self, playlist_id):
        def process_song_item(item):
            track = item.get('track')
            if track:
                return Song(name=track['name'], id=track['id'])
            return None  # Skip if track is missing

        # Use the paginator HOF to fetch and process all songs in the playlist
        return self._paginate(lambda limit, offset: self.sp.playlist_tracks(playlist_id, limit=limit, offset=offset), process_song_item)
    
    def update_playlist(self, playlist: Playlist):
        playlist_id = playlist.id
        # clear playlist
        self.sp.playlist_replace_items(playlist_id, [])
        # get uris and split into batches of 100
        song_uris = [f"spotify:track:{song.id}" for song in playlist.get_songs()]
        batches = [song_uris[i:i+100] for i in range(0, len(song_uris), 100)]
        # add each batch
        for batch in batches:
            self.sp.playlist_add_items(playlist_id, batch)