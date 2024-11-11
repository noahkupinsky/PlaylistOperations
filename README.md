# Playlist Operations

I found myself wishing there was a spotify feature that allowed me to designate a playlist as the combination of two others or similar, so I made it.

## Setup:

1) Clone the repo, make sure you've installed the libraries in *requirements.txt*, and make a *.env* file in the project root.
2) Create a spotify dev project (for web API) at https://developer.spotify.com. You probably want your redirect uri to be http://localhost:8888/callback for easy auth.
3) Add your **SPOTIFY_CLIENT_ID**, **SPOTIFY_CLIENT_SECRET**, and **SPOTIFY_REDIRECT_URI** to the env file.
4) Edit your playlist descriptions to set up your operations (see details below).
5) Run *main.py* (you'll be directed to a page where you need to click agree to use the Spotify API, but you'll only have to do this once ever).

## Details
Operations are created by denoting a particular playlist as the result of a group of operations *i*, and other playlists as contributors to that group. This will become clearer below.

Operations are deduced from the descriptions of the playlists on your spotify account. Each playlist may have a pair of square brackets, within which the playlist's operation commands are defined. 

All playlists are viewed as sets (in the math sense) of songs, which means the results of operations never have duplicates. **Any playlist that is not explicitly marked as the result of operations is not modified in any way. Any playlist that is marked as the result of operations will be completely cleared and reconstructed based on those operations!**

### Syntax

Playlists without square brackets are percieved to have no operation commands, and playlists with multiple pairs (ex. "\[blah\] \[blah\]"), nested pairs (ex. "\[blah\[blah\]\]"), or unbalanced pairs (ex. "\[blah\[blah\]") are ignored. Only playlists with one balanced pair of square brackets in their description will be parsed at all (ex. "This playlist is my life's work \[blah\]")

Operations tokens are a valid operation character (K, A, or R for now) followed by a number. Tokens may be comma separated, but do not have to be (but no comma is allowed between the letter and number). Whitespace is ignored. Anything other than a valid sequence of tokens will result in the playlist being ignored from operations entirely.

### Tokens

#### Key Playlists
Use a K, followed by a number *i* to mark a playlist as having key *i*. This will denote it as the result of operation group *i* (ex. K0). **If a key token is used in a playlist's operation commands, it must be the playlist's only token.** This prevents systems of equations, which is intentional. 

As mentioned above, any playlist without a key token won't be modified, and any playlist with a key token will be cleared, and rebuilt based on operations.

Whenever a number is used in a non-key token, it is required that a playlist with that key is somewhere in your account, otherwise an error will be thrown. Keys do not have to be sequential (you could have a playlist marked K8, a playlist marked K1293, and nothing else).

#### Addition
Use an A, followed by a number *i* to mark that all songs from this playlist should be added to the playlist with key *i* (ex. A0). For nerds: can be thought of as set union.

#### Subtraction/Removal
Use an R for remove ("removing songs" seems more natural than "subtracting songs"), followed by a number *i* to mark that all songs from this playlist should be removed from the playlist with key *i* (ex. R0). For nerds: can be thought of as set difference.

#### Order Of Operations

Spotify playlists are inherently unordered, so to reduce confusion, addition *always* takes precedence, and subtraction *always* comes last. So all songs from addition-marked playlists will be added, *and then* all songs from subtraction-marked playlists will be removed.

# Examples

## Examples Of Valid Descriptions
All of the following descriptions have tokens in an acceptable format, and will be parsed:

 - "I love tacos \[K0\]"
 - "I strongly dislike every song on this playlist \[R0R1 R2 , R3, R4\]"
 - "\[A0 R1\] Semi annoying shit"
 - "\[A123       \]"
 - "\[ K1\]"

## Examples Of Invalid Descriptions
All of these descriptions will result in the playlist being percieved as having no tokens

 - "No square brackets"
 - "Too many \[\[\[\]\]\]"
 - "Too many part two \[aaa\]\[sss\]"
 - "Wrong token format \[A0AR\]"
 - "Wrong token format part two \[A,0\]"

## Examples Of Valid Scenarios

### 1)

Playlist X description: "\[K0\]"

Playlist Y description: "\[A0\]"

Result: X = Y

### 2)

Playlist X description: "\[K0\]"

Playlist Y description: "\[A0\]"

Playlist Z description: "\[A0\]"

Result: X = Y + Z

### 3)

Playlist X description: "\[K0\]"

Playlist Y description: "\[A0\]"

Playlist Z description: "\[A0\]"

Playlist W description: "\[K1\]"

Playlist U description: "\[A0 A1\]"

Playlist V description: "\[A0 R1\]"

Result: 

X = Y + Z + U + V

W = U - V

### 4)

Playlist X description: "\[K0\]"

Playlist Y description: "\[A0\]"

Playlist Z description: "\[A0\]"

Playlist W description: "\[A0\]"

Playlist U description: "\[R0\]"

Playlist V description: "\[R0\]"

Result: X = (Y + Z + W) - U - V

### 5)
The following is a good demonstrator of how the operations reflect union and difference, as well as the precedence.

Playlist X description: "\[K0\]"

Playlist Y description: "\[A0\]"

Playlist Z description: "\[A0 R0\]"

Result: X = (Y + Z) - Z = Y - Z

### 6)
Playlist X description: "\[K0\]"

Result: X becomes empty

## Examples Of Invalid Scenarios
These scenarios will throw an error

### 1)

Playlist X description: "\[K0 A1\]"

Playlist Y description: "\[K1\]"

Playlist Z description: "\[A0\]"

Error: K0 must be alone

### 2)

Playlist X description: "\[K0\]"

Playlist Y description: "\[A1\]"

Playlist Z description: "\[A0\]"

Error: no K1 found


