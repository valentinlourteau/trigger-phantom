from flask import Flask, jsonify
import os
import requests
import base64

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("SPOTIFY_REFRESH_TOKEN")
DEVICE_ID = os.getenv("SPOTIFY_DEVICE_ID")
PLAYLIST_URI = os.getenv("SPOTIFY_PLAYLIST_URI")
VOLUME = int(os.getenv("SPOTIFY_VOLUME", 40))

app = Flask(__name__)

def get_access_token():
    auth = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN
    }
    r = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    r.raise_for_status()
    return r.json()["access_token"]

@app.route("/launch")
def launch_love_capsule():
    token = get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Set volume
    requests.put(
        f"https://api.spotify.com/v1/me/player/volume?volume_percent={VOLUME}&device_id={DEVICE_ID}",
        headers=headers
    )

    # Play playlist
    requests.put(
        f"https://api.spotify.com/v1/me/player/play?device_id={DEVICE_ID}",
        headers=headers,
        json={"context_uri": PLAYLIST_URI}
    )

    return jsonify({"status": "🎶 Love capsule lancé 🔥"})

@app.route("/")
def home():
    return "Webhook prêt à lancer la Love Capsule 💘"
