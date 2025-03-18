import openai
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import time

# Load environment variables from .env
load_dotenv()

# OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Spotify Authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    scope="user-modify-playback-state user-read-playback-state"
))

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Fetch and refine song search
def search_spotify(song_name, artist_name=None):
    query = f"track:{song_name}"
    if artist_name:
        query += f" artist:{artist_name}"
    
    results = sp.search(q=query, type='track', limit=3)
    
    if results['tracks']['items']:
        return results['tracks']['items'][0]  # Best match
    return None

# Validate with ChatGPT
def validate_song_with_gpt(user_input, spotify_result):
    gpt_prompt = f"""
    The user searched for: "{user_input}". 
    The top Spotify result is "{spotify_result['name']}" by "{', '.join(artist['name'] for artist in spotify_result['artists'])}". 
    Is this likely the intended song? Reply "yes" or "no".
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": gpt_prompt}]
    )
    return response.choices[0].message.content.strip().lower() == "yes"

# Play the best match on Spotify
def play_spotify_track(song_name, artist_name=None):
    attempts = 3  # Allow refining up to 3 times
    while attempts > 0:
        spotify_result = search_spotify(song_name, artist_name)
        if not spotify_result:
            return "Couldn't find that track, boss."
        
        if validate_song_with_gpt(song_name, spotify_result):
            sp.start_playback(uris=[spotify_result['uri']])
            return f"Playing '{spotify_result['name']}' by {', '.join(artist['name'] for artist in spotify_result['artists'])} on Spotify."
        
        # Modify query and retry
        song_name = spotify_result['name']
        artist_name = spotify_result['artists'][0]['name']
        attempts -= 1
        time.sleep(1)
    
    return "Couldn't confidently determine the song, boss."