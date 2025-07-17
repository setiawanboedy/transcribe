import requests
import os

# --- Configuration ---
# Make sure this URL matches your Flask server's address and port
SERVER_URL = "http://127.0.0.1:5000/transcribe"

# --- Path to your test audio file ---
# Adjust this path based on where you saved your test audio file
# Example if your audio is in a 'test_data' folder relative to test_client.py:
AUDIO_FILE_PATH = "./audio_sample.wav"
# Or a direct path:
# AUDIO_FILE_PATH = "/Users/youruser/Documents/faster_whisper_server/test_data/example_audio.wav"

if not os.path.exists(AUDIO_FILE_PATH):
    print(f"Error: Audio file not found at {AUDIO_FILE_PATH}")
    print("Please create an audio file (e.g., example_audio.wav) or update AUDIO_FILE_PATH.")
    exit(1)

print(f"Attempting to send {AUDIO_FILE_PATH} to {SERVER_URL}...")

try:
    # Open the audio file in binary read mode
    with open(AUDIO_FILE_PATH, 'rb') as f:
        # Prepare the files dictionary for requests.post
        # The key 'audio_file' must match the name expected by Flask (request.files['audio_file'])
        # The tuple format is (filename, file_object, content_type)
        files = {'audio_file': (os.path.basename(AUDIO_FILE_PATH), f, 'audio/wav')}

        # Send the POST request
        response = requests.post(SERVER_URL, files=files)

    # --- Process the response ---
    if response.status_code == 200:
        print("\n--- Transcription Successful! ---")
        print("Response JSON:")
        print(response.json())
        print(f"Transcribed Text: {response.json().get('transcription', 'N/A')}")
    else:
        print(f"\n--- Error: Server returned status code {response.status_code} ---")
        print("Response Text:")
        print(response.text)
        try:
            print("Response JSON (if any):")
            print(response.json())
        except requests.exceptions.JSONDecodeError:
            print("Response is not valid JSON.")

except requests.exceptions.ConnectionError:
    print(f"\n--- Connection Error ---")
    print(f"Could not connect to the server at {SERVER_URL}.")
    print("Please ensure your Flask server (app.py) is running in another terminal.")
except Exception as e:
    print(f"\n--- An unexpected error occurred ---")
    print(e)