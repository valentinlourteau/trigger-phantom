from flask import Flask, request, jsonify
import requests
import base64
import os

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("SPOTIFY_REFRESH_TOKEN")
DEVICE_ID = os.getenv("SPOTIFY_DEVICE_ID")
PLAYLIST_URI = os.getenv("SPOTIFY_PLAYLIST_URI")
VOLUME = int(os.getenv("SPOTIFY_VOLUME", 40))

app = Flask(__name__)

def get_access_token():
    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    headers = {
        "Authorization": f"Basic {b64_auth_str}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN
    }

    r = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    r.raise_for_status()
    return r.json()["access_token"]

@app.route("/launch", methods=["GET"])
def launch():
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

    return jsonify({"status": "love capsule launched 💘"})

@app.route("/", methods=["GET"])
def home():
    return "Ready to launch the Love Capsule 🚀"

if __name__ == "__main__":
    app.run()
