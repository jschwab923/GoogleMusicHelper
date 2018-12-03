from flask import Flask, request, redirect, g, render_template, make_response, jsonify
import urllib

from SpotifyHelper import SpotifyHelper
from GoogleMusicHelper import GoogleMusicHelper

app = Flask(__name__)

#  Client Keys
CLIENT_ID = "eab2f986cd8846b8b210073e366ef2f5"
CLIENT_SECRET = "545abe0dc6464c47b2976e0f915fc6a1"

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# Server-side Parameters
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 8080
REDIRECT_URI = "{}:{}/spotify/callback/q".format(CLIENT_SIDE_URL, PORT)
SCOPE = "playlist-modify-public playlist-modify-private"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "client_id": CLIENT_ID
}

google_helper = GoogleMusicHelper()
spotify_helper = SpotifyHelper()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/google/login")
def google_login():
    email = "jschwab923@gmail.com"
    password = "@Didgyreandgimble923"
    google_helper = GoogleMusicHelper()
    return google_helper.login(email, password)

@app.route("/google/playlists")
def google_playlists():
    google_login()
    return jsonify(google_helper().list_playlists())

@app.route("/spotify/login")
def spotify_login():
    url_args = "&".join(["{}={}".format(key, urllib.quote(val)) for key, val in auth_query_parameters.iteritems()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)

@app.route("/spotify/playlists")
def spotify_playlists():
    access_token = request.cookies.get('access_token', None)
    if not access_token:
        return redirect("/")

    spotify_helper = SpotifyHelper(access_token)
    return jsonify(spotify_helper.list_playlists())

@app.route("/spotify/tracks")
def spotify_tracks():
    access_token = request.cookies.get('access_token', None)
    if not access_token:
        return redirect("/")

    spotify_helper = SpotifyHelper(access_token)
    return jsonify(spotify_helper.user_library_tracks())

@app.route("/spotify/search")
def search_spotify(song=None, artist=None):
    access_token = request.cookies.get('access_token', None)
    if not access_token:
        return redirect("/")

    spotify_helper = SpotifyHelper(access_token)
    return jsonify(spotify_helper.search_for_song("Blame It On Me", "Calvin Harris"))

@app.route("/spotify/callback/q")
def spotify_callback():
    spotify_helper = SpotifyHelper()
    response_data = spotify_helper.authorize(request.args['code'])
    access_token = response_data["access_token"]
    # refresh_token = response_data["refresh_token"]
    # token_type = response_data["token_type"]
    # expires_in = response_data["expires_in"]

    resp = make_response(redirect("/"))
    resp.set_cookie(key="access_token", value=access_token)

    return resp

def google_helper():
    email = "jschwab923@gmail.com"
    password = "@Didgyreandgimble923"
    google_helper = GoogleMusicHelper()
    google_helper.login(email, password)
    return google_helper

if __name__ == "__main__":
    app.run(debug=True, port=PORT)
