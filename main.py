from bs4 import BeautifulSoup
import requests
from auth import *
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = input("Which date do you want to travel to? Type the date in this format YYYY-MM-DD: ")

URL = f"https://www.billboard.com/charts/hot-100/{date}/"

response = requests.get(URL)

billboard_hot_100_web_page = response.text

soup = BeautifulSoup(billboard_hot_100_web_page, "html.parser")
songs_list = soup.find_all(name="h3", class_='a-no-trucate')
songs = [song.getText().strip() for song in songs_list]
artists_list = soup.find_all(name="span", class_='a-no-trucate')
artists = [artist.getText().strip() for artist in artists_list]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri="http://example.com",
                              scope="playlist-modify-private", show_dialog=True,
                              cache_path="token.txt"))

user_id = sp.current_user()["id"]

song_uris = []
for i in range(len(songs)):
    result = sp.search(q=f"{songs[i]} {artists[i]}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{songs[i]} doesn't exist in Spotify. Skipped.")

new_playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False, collaborative=False,
                                       description='')

sp.playlist_add_items(playlist_id=new_playlist["id"], items=song_uris, position=None)
