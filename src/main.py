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


# Main execution
playlist_name = "Radio Memo Test"
existing_playlists = spotify.get_all_playlists(sp)

# Check if the playlist already exists and clear it if so
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

# Create a new playlist and add liked tracks
# create_playlist_and_add_tracks(playlist_name)
# print("Playlist created successfully!")