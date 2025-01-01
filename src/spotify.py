# import logging
import os

import spotipy
import spotipy.util

from dotenv import load_dotenv
load_dotenv()


# Login to Spotify
def login(username='mbirgi', scope='user-library-read'):
    spotify_auth_params = {
        'client_id': os.getenv('CLIENT_ID'),
        'client_secret': os.getenv('CLIENT_SECRET'),
        'redirect_uri': os.getenv('REDIRECT_URI'),
        'scope': scope
    }
    try:
        token = spotipy.util.prompt_for_user_token(username, **spotify_auth_params)
    except:
        os.remove(f'.cache-{username}')
        token = spotipy.util.prompt_for_user_token(username, **spotify_auth_params)
    return spotipy.Spotify(auth=token)


# Function to get liked tracks
def get_liked_tracks():
    results = sp.current_user_saved_tracks(limit=50)
    track_uris = []

    while results:
        for item in results['items']:
            track = item['track']
            track_uris.append(track['uri'])  # Collect track URIs
        if results['next']:
            results = sp.next(results)
        else:
            break

        return track_uris


# Function to get all user playlists with pagination
def get_all_playlists():
    playlists = []
    results = sp.current_user_playlists(limit=50)  # Start with the first page

    while results:
        playlists.extend(results['items'])  # Add current page items to the list
        if results['next']:
            results = sp.next(results)  # Go to the next page
        else:
            break

    return playlists


# Function to clear existing playlist
def clear_playlist(playlist_id):
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



