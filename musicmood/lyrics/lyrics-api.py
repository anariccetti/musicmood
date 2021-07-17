import numpy as np
import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyClientCredentials
import os
import re
import pandas as pd
import string 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize



class MusicData():

    def __init__(self):
        self.client = os.getenv('SPOTIPY_CLIENT_ID')
        self.secret = os.getenv('SPOTIPY_CLIENT_SECRET')

    def scrape_lyrics(self, artistname, songname, i=0):
        artistname_clean = str(artistname.replace(' ','-')) if ' ' in artistname else str(artistname)
        songname_clean = str(songname.replace(' ','-')) if ' ' in songname else str(songname)
        page = requests.get('https://genius.com/'+ artistname_clean + '-' + songname_clean + '-' + 'lyrics')
        html = BeautifulSoup(page.text, 'html.parser')
        lyrics1 = html.find("div", class_="lyrics")
        lyrics2 = html.find("div", class_="Lyrics__Container-sc-1ynbvzw-2 jgQsqn")
        if lyrics1:
            lyrics = lyrics1.get_text()
        elif lyrics2:
            lyrics = lyrics2.get_text()

        elif lyrics1 == lyrics2 == None and i  < 3:
            i += 1
            lyrics = self.scrape_lyrics(artistname.title(), songname.title(), i)
        else:
            print("Lyrics Not Fund")
            lyrics = None
        return lyrics


    def search_spotify(self, query):
        print(self.client, self.secret)
        spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=self.client, client_secret=self.secret))
        results = spotify.search(q='track:' + query, type='track')
        return results

    def to_lower_case(lyrics):
        results = lyrics.lower()

    def remove_lyrics_observations(lyrics):
        results = re.sub(r'\[[^()]*\]', '', lyrics)
    
    def remove_punctuation(lyrics):
        for punctuation in string.punctuation:
            results = lyrics.replace(punctuation, '') 

    def remove_stop_words(self,lyrics):
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(lyrics)
        lyrics = [w for w in word_tokens if not w in stop_words]
        return lyrics

    def get_clean_song(self,artistname, songname):
        lyrics = self.scrape_lyrics(artistname, songname)

        lyrics = self.remove_lyrics_observations(lyrics)

        lyrics = self.remove_punctuation(lyrics)

        lyrics = self.remove_stop_words(lyrics)

        return lyrics

    def export_playlist_data(self):
        spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=self.client, client_secret=self.secret))

        playlists = spotify.playlist('spotify:playlist:37i9dQZF1DX3oM43CtKnRV')
        

        data = {"track":[],
                "artist":[],
                "lyrics":[]}
        
        for track in playlists['tracks']['items']:
            data['track'].append(track['track']['name'])
            data['artist'].append(track['track']['artists'][0]['name'])
            data['lyrics'].append(self.scrape_lyrics(track['track']['artists'][0]['name'], track['track']['name'], i=0))
        
        
        df = pd.DataFrame(data)

        df.to_csv("rock00s_v2.csv",index=False)

# print(MusicData().scrape_lyrics("metallica", "fuel"))
# print(MusicData().scrape_lyrics("Metallica", "creeping death"))
# print(MusicData().search_spotify('hysteria'))


if __name__ == '__main__':
    # print(MusicData().search_spotify('hysteria'))
    print(MusicData().export_playlist_data())

