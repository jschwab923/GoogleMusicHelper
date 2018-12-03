from flask import jsonify
from gmusicapi import Mobileclient


class GoogleMusicHelper(object):

    def __init__(self, email=None, password=None):
        self.google_music_client = Mobileclient()
        if email and password:
            self.login(email, password)

    def login(self, email, password):
        if self.google_music_client.login(email, password, Mobileclient.FROM_MAC_ADDRESS):
            return "Logged in to Google"
        return "Error logging in"

    def add_song_by_name_to_google_library(self, song="", artist=""):
        results = self.google_music_client.search(query=song + " " + artist, max_results=1)
        if results:
            track = results["song_hits"][0]["track"]
            return self.google_music_client.add_store_tracks(track.get("storeId") or track.get("nid"))

    def list_playlists(self):
        return self.google_music_client.get_all_user_playlist_contents()

    def sync_playlists_with_library(self, password=None, username=None):
        if self.google_music_client.login(username, password, Mobileclient.FROM_MAC_ADDRESS):
            all_tracks = []
            for playlist in self.google_music_client.get_all_user_playlist_contents():
                for track in playlist["tracks"]:
                    all_tracks.append(track["track"])

            playlist_store_ids = [track["storeId"] for track in all_tracks]
            all_songs = self.google_music_client.get_all_songs(incremental=False)

            print all_songs[0]

            added_store_ids = []
            for song in all_songs:
                store_id = None
                if song.get("nid"):
                    store_id = song["nid"]
                elif song.get("storeId"):
                    store_id = song["storeId"]
                added_store_ids.append(store_id)

            new_store_ids = set(playlist_store_ids) - set(added_store_ids)
            new_tracks = [track for track in all_tracks if track["storeId"] not in added_store_ids]
            for storeId in new_store_ids:
                for track in new_tracks:
                    if track["storeId"] == storeId:
                        break
                print track['title'] + " by " + track["artist"]
                print self.google_music_client.add_store_tracks(storeId)
