from package.music_objects import Playlist
from package.playlist_operations import *
from package.utils import lex_operation_tokens, Token

class PlaylistOperator:
    def __init__(self, playlists: list[Playlist]):
        self.playlist_dict = {}
        self.playlists = playlists
        self.operations = []

    def parse_token(self, token: Token, playlist: Playlist):
        token_letter, token_number = token
        # setting key for playlist
        if token_letter == "K":
            if token_number in self.playlist_dict:
                raise ValueError("Duplicate key found")
            self.playlist_dict[token_number] = playlist
            # playlist is cleared to be defined exactly by tokens
            playlist.clear()
        # adding playlist to another
        elif token_letter == "A":
            add_operation = PlaylistOperationAdd(playlist, lambda: self.playlist_dict[token_number])
            self.operations.append(add_operation)
        # removing playlist from another
        elif token_letter == "R":
            remove_operation = PlaylistOperationRemove(playlist, lambda: self.playlist_dict[token_number])
            self.operations.append(remove_operation)

    def operate(self):
        for playlist in self.playlists:
            tokens = lex_operation_tokens(playlist.name)

            key_set_tokens = list(filter(lambda token: token[0] == "K", tokens))
            if len(key_set_tokens) > 1:
                raise ValueError("Multiple key tokens found")
            
            for token in tokens:
                self.parse_token(token, playlist)

        self.operations.sort()
        
        for operation in self.operations:
            operation.execute()