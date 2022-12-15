from pprint import pprint
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

billboard_url = "https://www.billboard.com/charts/hot-100/1996-03-21/"
spotify_client_id = '123'
spotify_client_secret = 'abc'
app_name = 'desired date'

# Get top 100 songs from Billboard hot 100 for specified data
html = BeautifulSoup(requests.get(billboard_url).text, 'html.parser')
songs_list = [song.getText().strip() for song in html.select(selector="li ul li h3")]
# print(songs_list)

# Connect to Spotify App
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private", redirect_uri="http://example.com", client_id=spotify_client_id,
        client_secret=spotify_client_secret, show_dialog=True, cache_path="token.txt"
    )
)

# Create playlist
user_id = sp.current_user()["id"]
# playlist = sp.user_playlist_create(user=user_id, name=f"{app_name} Billboard 100", public=False)

# Search for top 100 songs in Spotify
songs_uris = []
for song in songs_list:
    results = sp.search(q=f"track: {song} year: 1996", limit=1, type="track")
    try:
        uri = results["tracks"]["items"][0]["uri"]
        songs_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

sp.playlist_add_items(playlist_id=playlist["id"], items=songs_uris)



