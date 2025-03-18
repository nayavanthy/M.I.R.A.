import os
import openai
from dotenv import load_dotenv
import json
import requests

import app_launcher
import music_handler

# Load environment variables from .env
load_dotenv()

# OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def preliminary_interpret(message):
    """Classifies user input as a command (app/music) or general conversation."""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[ 
                {"role": "system", "content": "You are a preliminary message checking finction for an AI assistant"},
                {"role": "user", "content": f"Interpret the message to see if it is a direct command like: "
                                            f"1. It is an app launch command (e.g., 'run notepad'). "
                                            f"2. It is a direct Spotify command (e.g., 'play Blinding Lights by The Weeknd'). "
                                            f"If it is either of the above, i.e. asking to open an app or play something on spotify reply yes, else reply no"
                                            f"Reply strictly with one word, 'yes' or 'no'"
                                            f"The message is: '{message}'"}
            ]
        )

        classification = response.choices[0].message.content.strip().lower()

        if classification == "yes":
            interpreted = interpret_command(message)
            return process_command(interpreted)
        elif classification == "no":
            return send_to_backend(message)
        else:
            return "Error: Unexpected classification response."

    except Exception as e:
        return f"Error: {str(e)}"
    
def send_to_backend(message):
    """Forwards general chat messages to the FastAPI backend."""
    try:
        response = requests.post(
            "http://127.0.0.1:8000/chat",
            json={"message": message},
            timeout=10
        )
        response_data = response.json()
        return response_data.get("response", "No response from server.")
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

def interpret_command(command):
    """Interpret the user's command and classify it as opening an app or playing music."""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are MIRA, an AI that executes commands for applications and Spotify."},
            {"role": "user", "content": f"""Interpret this command and return a JSON:
                {{"type": "application" or "music", "name": "<app/song/album>", "artist": "<mandatory>"}}

                Only output the json string. Use fuzzy logic to correct mistakes and fill in empty feilds
                Example:
                Input: 'play Blinding Lights by The Weeknd' 
                Output: {{"type": "music", "name": "Blinding Lights", "artist": "The Weeknd"}}

                Input: 'launch Photoshop' 
                Output: {{"type": "application", "name": "Photoshop"}}
                
                Now interpret: '{command}'
            """}
        ]
    )
    
    try:
        parsed_response = json.loads(response.choices[0].message.content.strip())
        return parsed_response
    except json.JSONDecodeError:
        return {"type": "unknown", "name": ""}

def process_command(interpreted):
    if interpreted["type"] == "application":
        return app_launcher.open_application(interpreted["name"])
    elif interpreted["type"] == "music":
        return music_handler.play_spotify_track(interpreted["name"], interpreted.get("artist"))
    else:
        return "I'm not sure how to do that yet, boss."

# Example usage
if __name__ == "__main__":
    while True:
        cmd = input("You: ")
        if cmd.lower() == "exit":
            break
        print(f"MIRA: {preliminary_interpret(cmd)}")
