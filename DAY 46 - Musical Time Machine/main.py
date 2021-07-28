import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
from decouple import config

# authorizing Spotify
CLIENT_ID = config("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = config("SPOTIFY_CLIENT_SECRET")

scope = "playlist-modify-private"
sp = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri="https://example.com", scope=scope)
spotify = spotipy.Spotify(auth_manager=sp)

# get user id of current user authenticated
USER_ID = spotify.current_user()["id"]


# Scraping website for top 100 songs in given time
year = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:\n")

try:
    response = requests.get(f"https://www.billboard.com/charts/hot-100/{year}")
    response.raise_for_status()
except requests.exceptions.HTTPError:
    print("There was an error. Are you sure you inputted in the correct format?")
else:

    # make a soup from the billboard webpage
    billboard_webpage = response.text
    soup = BeautifulSoup(billboard_webpage, "html.parser")

    # make two separate lists for song titles and corresponding artists from webpage information
    songs = (title.text for title in soup.find_all("span", class_="chart-element__information__song text--truncate color--primary"))
    artists = (artist.text for artist in soup.find_all("span", class_="chart-element__information__artist text--truncate color--secondary"))

    # make a dictionary out of the created two lists
    songs_dict = dict(zip(songs, artists))
    songs_uris = []

    for key, value in songs_dict.items():
        song = key.lower()
        artist = value.lower().split("featuring")[0]

        search_results = spotify.search(q=f"{song} {artist}")["tracks"]["items"]
        
        found = False

        # exception handling when results aren't on spotify or when there aren't any
        try:
            results = (item for item in search_results)
        except IndexError:
            continue
        else:
            for item in results:
                for people in item["artists"]:
                    if (people["name"].lower() in value.lower() or artist in people["name"].lower()) and (song in item["name"].lower() or item["name"].lower() in song):
                        songs_uris.append(item["uri"])
                        found = True
                        break
                
                if found:
                    break
    
    print(len(songs_uris))

    playlist_id = spotify.user_playlist_create(USER_ID, year, description="The 100 top songs of ugh.", public=False)["uri"]

    spotify.user_playlist_add_tracks(USER_ID, playlist_id, songs_uris)