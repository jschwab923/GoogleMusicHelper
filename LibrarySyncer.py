from GoogleMusicHelper import GoogleMusicHelper
from SpotifyHelper import SpotifyHelper


def sync_libraries():
    google_helper = GoogleMusicHelper(email="", password="")
    print google_helper.add_song_by_name_to_google_library(song="Figures", artist="Jessie Reyez")


if __name__ == '__main__':
    sync_libraries()
