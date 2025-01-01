import spotify
import utils

# login
sp = spotify.login(
    scope=(
        'playlist-read-private '
        'playlist-modify-private '
        'playlist-modify-public '
        'user-library-read'
    )
)
user = sp.current_user()

# check login success:
# displayName = user['display_name']
# print(displayName)


# Check if the playlist already exists and clear it if so
existing_playlists = spotify.get_all_playlists(sp)
playlist_name = "Radio Memo Test"
for playlist in existing_playlists:
    # print(playlist['name'])
    if playlist['name'] == playlist_name:
        print(f"found playlist '{playlist_name}', clearing")
        spotify.clear_playlist(sp, playlist['id'])
        target_playlist = playlist
        break

# If the playlist doesn't exist, create it
if 'target_playlist' not in locals():
    print(f"playlist '{playlist_name}' not found, creating")
    target_playlist = sp.user_playlist_create(user['id'], playlist_name, public=True)

# Get liked tracks
liked_tracks = spotify.get_liked_tracks(sp)
print(f"Found {len(liked_tracks)} liked tracks")

# Add liked tracks to the playlist in batches
track_uris = [track['track']['uri'] for track in liked_tracks]
batch_size = 100

for i in range(0, len(track_uris), batch_size):
    sp.playlist_add_items(target_playlist['id'], track_uris[i:i + batch_size])
    print(f"Added {min(i + batch_size, len(liked_tracks))} tracks to playlist")

print("All liked tracks added to the playlist successfully!")
