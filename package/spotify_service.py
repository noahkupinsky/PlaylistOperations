from abc import ABC, abstractmethod
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables from .env file
load_dotenv()

class BaseSpotifyService(ABC):
    def __init__(self):
        """
        Initialize the class and set up the Spotify instance and user ID.
        """
        self.sp = self._create_spotify_instance()
        self.user_id = self._get_user_id()

    @abstractmethod
    def _create_spotify_instance(self):
        """
        Create and return a Spotify instance with proper authentication.
        """
        pass

    @abstractmethod
    def _get_user_id(self):
        """
        Retrieve and return the user ID of the authenticated user.
        """
        pass

    @abstractmethod
    def get_playlists(self):
        """
        Retrieve and return all playlists owned by the authenticated user, handling pagination.
        """
        pass

    def _is_owned_by_user(self, playlist):
        """
        Check if a playlist is owned by the user.
        """
        return playlist.get('owner', {}).get('id') == self.user_id


class SpotifyService(BaseSpotifyService):
    def _create_spotify_instance(self):
        """
        Initialize the Spotify instance with proper authentication.
        """
        return spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIFY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
            scope="playlist-modify-public playlist-modify-private playlist-read-private"
        ))

    def _get_user_id(self):
        """
        Retrieve the user ID of the authenticated user.
        """
        user_profile = self.sp.current_user()
        return user_profile['id']

    def get_playlists(self):
        """
        Retrieve all playlists owned by the authenticated user.
        """
        playlists = []
        results = self.sp.current_user_playlists(limit=50)
        playlists.extend(results['items'])

        # Paginate through all playlists
        while results['next']:
            results = self.sp.next(results)
            playlists.extend(results['items'])

        # Filter to only include playlists owned by the user
        user_owned_playlists = [playlist for playlist in playlists if self._is_owned_by_user(playlist)]
        return user_owned_playlists