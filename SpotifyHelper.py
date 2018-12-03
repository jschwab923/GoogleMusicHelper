# shows a user's playlists (need to be authenticated via oauth)
import base64
import urllib

import requests
import json

#  Client Keys
import spotipy

CLIENT_ID = "eab2f986cd8846b8b210073e366ef2f5"
CLIENT_SECRET = "545abe0dc6464c47b2976e0f915fc6a1"

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 8080
REDIRECT_URI = "{}:{}/spotify/callback/q".format(CLIENT_SIDE_URL, PORT)


class SpotifyHelper(object):

    def __init__(self, access_token=None):
        self.access_token = access_token

    def user_library_tracks(self):
        authorization_header = {"Authorization": "Bearer {}".format(self.access_token)}
        user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
        profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
        profile_data = json.loads(profile_response.text)

        playlist_api_endpoint = "{}/tracks".format(profile_data["href"])
        playlists_response = requests.get(playlist_api_endpoint, headers=authorization_header)
        return playlists_response.json()

    def search_for_song(self, song=None, artist=None):
        search_endpoint = "{}/search?q={}&type=track".format(SPOTIFY_API_URL,
                                                             urllib.quote_plus(song + " " + artist))
        authorization_header = {"Authorization": "Bearer {}".format(self.access_token)}

        request = requests.get(search_endpoint, headers=authorization_header)
        return json.loads(request.text)

    def list_playlists(self):
        authorization_header = {"Authorization": "Bearer {}".format(self.access_token)}
        user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
        profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
        profile_data = json.loads(profile_response.text)

        playlist_api_endpoint = "{}/playlists".format(profile_data["href"])
        playlists_response = requests.get(playlist_api_endpoint, headers=authorization_header)
        return playlists_response.json()

    def authorize(self, auth_token=None):
        code_payload = {
            "grant_type": "authorization_code",
            "code": str(auth_token),
            "redirect_uri": REDIRECT_URI,
            "scope": "user-library-read user-library-modify playlist-read-private playlist-modify-private"
        }
        base64encoded = base64.b64encode("{}:{}".format(CLIENT_ID, CLIENT_SECRET))
        headers = {"Authorization": "Basic {}".format(base64encoded)}
        post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

        return json.loads(post_request.text)


if __name__ == '__main__':
    helper = SpotifyHelper()
    helper.list_playlists()
