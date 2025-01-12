import spotipy
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
playlist_id = "2H8Wus9KXf7WGg9rbXLy9e"
target_playlist = None

for attempt in range(10):
    try:
        target_playlist = sp.playlist(playlist_id)
        logging.info(f"Found playlist '{target_playlist['name']}' with id {playlist_id}, clearing")
        spotify_utils.clear_playlist(sp, playlist_id)
        break
    except spotipy.exceptions.SpotifyException as e:
        logging.info(f"Attempt {attempt + 1}: Playlist with id {playlist_id} not found, retrying in 5 seconds...")
        time.sleep(5)

if not target_playlist:
    logging.info(f"Playlist with id {playlist_id} not found after 10 attempts, creating a new playlist")
    target_playlist = sp.user_playlist_create(user['id'], "Radio Memo", public=True)
    playlist_id = target_playlist['id']
    logging.info(f"Created new playlist '{target_playlist['name']}' with id {playlist_id}")

# Add liked tracks to the playlist in batches
track_uris = [track['track']['uri'] for track in liked_tracks]
batch_size = 100
logging.info(f"Adding {len(track_uris)} liked tracks to the playlist")
for i in tqdm(range(0, len(track_uris), batch_size), desc="Adding tracks", unit="batch"):
    sp.playlist_add_items(playlist_id, track_uris[i:i + batch_size])

logging.info("All liked tracks added to the playlist successfully!")
logging.info("**** Script complete")
