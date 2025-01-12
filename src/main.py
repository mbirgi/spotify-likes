import spotify_utils
from tqdm import tqdm
import logging
import os
import time

# Configure logging
log_file_path = os.path.expanduser('~/logs/spotify_likes.log')
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
logging.basicConfig(filename=log_file_path, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("====================")
logging.info("**** Starting script")

# login
sp = spotify_utils.login()
user = sp.current_user()
logging.info(f"Logged in as {user['display_name']}")

# Get liked tracks
liked_tracks = spotify_utils.get_liked_tracks(sp)
logging.info(f"Found {len(liked_tracks)} liked tracks")

# Check if the playlist already exists and clear it if so
playlist_name = "Radio Memo"
target_playlist = None

for attempt in range(10):
    existing_playlists = spotify_utils.get_all_playlists(sp)
    logging.info(f"Attempt {attempt + 1}: Found {len(existing_playlists)} existing playlists")
    
    for playlist in existing_playlists:
        if playlist['name'].lower() == playlist_name.lower():
            logging.info(f"Found playlist '{playlist_name}' with id {playlist['id']}, clearing")
            spotify_utils.clear_playlist(sp, playlist['id'])
            target_playlist = playlist
            break
    
    if target_playlist:
        break
    else:
        logging.info(f"Playlist '{playlist_name}' not found, retrying in 5 seconds...")
        time.sleep(5)

if not target_playlist:
    logging.info(f"Playlist '{playlist_name}' not found after 10 attempts, creating")
    target_playlist = sp.user_playlist_create(user['id'], playlist_name, public=True)

# Add liked tracks to the playlist in batches
track_uris = [track['track']['uri'] for track in liked_tracks]
batch_size = 100
logging.info(f"Adding {len(track_uris)} liked tracks to the playlist")
for i in tqdm(range(0, len(track_uris), batch_size), desc="Adding tracks", unit="batch"):
    sp.playlist_add_items(target_playlist['id'], track_uris[i:i + batch_size])

logging.info("All liked tracks added to the playlist successfully!")
logging.info("**** Script complete")
