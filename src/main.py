import spotify
import utils

# login
sp = spotify.login(
    scope='playlist-read-private playlist-modify-private user-library-read'
)
user = sp.current_user()

# check login success:
# displayName = user['display_name']
# print(displayName)


# Main execution
playlist_name = "Radio Memo"
existing_playlists = get_all_playlists()

# Check if the playlist already exists and clear it if so
for playlist in existing_playlists['items']:
    print(playlist['name'])
    # if playlist['name'] == playlist_name:
    #     print(f"found playlist '{playlist_name}', clearing")
    #     clear_playlist(playlist['id'])
    #     break

# Create a new playlist and add liked tracks
# create_playlist_and_add_tracks(playlist_name)
# print("Playlist created successfully!")