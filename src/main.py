import spotify
import utils
from tqdm import tqdm

# login
sp = spotify.login()
user = sp.current_user()

# Check if the playlist already exists and clear it if so
existing_playlists = spotify.get_all_playlists(sp)
playlist_name = "Radio Memo"
target_playlist = None
for playlist in existing_playlists:
    if playlist['name'].lower() == playlist_name.lower():
        print(f"found playlist '{playlist_name}', clearing")
        spotify.clear_playlist(sp, playlist['id'])
        target_playlist = playlist
        break

# If the playlist doesn't exist, create it
if target_playlist is None:
    print(f"playlist '{playlist_name}' not found, creating")
    target_playlist = sp.user_playlist_create(user['id'], playlist_name, public=True)

# Get liked tracks
liked_tracks = spotify.get_liked_tracks(sp)
print(f"Found {len(liked_tracks)} liked tracks")

# Add liked tracks to the playlist in batches
track_uris = [track['track']['uri'] for track in liked_tracks]
batch_size = 100

for i in tqdm(range(0, len(track_uris), batch_size), desc="Adding tracks", unit="batch"):
    sp.playlist_add_items(target_playlist['id'], track_uris[i:i + batch_size])

print("All liked tracks added to the playlist successfully!")
