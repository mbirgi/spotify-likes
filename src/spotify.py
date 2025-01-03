import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

def login():
    sp_oauth = SpotifyOAuth(
        client_id=os.getenv('CLIENT_ID'),
        client_secret=os.getenv('CLIENT_SECRET'),
        redirect_uri=os.getenv('REDIRECT_URI'),
        scope='user-library-read playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public',
        cache_path='.cache'
    )
    
    token_info = sp_oauth.get_cached_token()
    
    if not token_info:
        auth_url = sp_oauth.get_authorize_url()
        print(f'Please navigate here: {auth_url}')
        response = input('Enter the URL you were redirected to: ')
        code = sp_oauth.parse_response_code(response)
        token_info = sp_oauth.get_access_token(code)
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    return sp


# Function to get liked tracks
def get_liked_tracks(sp):
    results = sp.current_user_saved_tracks(limit=50)
    tracks = results['items']
    total = results['total']
    
    with tqdm(total=total, desc="Fetching liked tracks", unit="track") as pbar:
        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])
            pbar.update(len(results['items']))
    
    return tracks


# Function to get all user playlists with pagination
def get_all_playlists(sp):
    playlists = []
    results = sp.current_user_playlists(limit=50)
    playlists.extend(results['items'])
    
    while results['next']:
        results = sp.next(results)
        playlists.extend(results['items'])
    
    return playlists


# Function to clear existing playlist
def clear_playlist(sp, playlist_id):
    sp.playlist_replace_items(playlist_id, [])
    print(f"Cleared playlist with ID: {playlist_id}")


# Function to create a new playlist and add liked tracks in batches
def create_playlist_and_add_tracks(playlist_name):
    # Create a new playlist
    user_id = sp.current_user()['id']
    new_playlist = sp.user_playlist_create(user_id, playlist_name, public=False)
    
    # Get liked tracks
    track_uris = get_liked_tracks()

    # Add tracks to the new playlist in batches of 100
    if track_uris:
        for i in range(0, len(track_uris), 100):
            batch = track_uris[i:i + 100]  # Get the next batch of up to 100 tracks
            sp.playlist_add_items(new_playlist['id'], batch)
            print(f"Added {len(batch)} liked tracks to '{playlist_name}'.")



