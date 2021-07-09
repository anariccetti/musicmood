import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyClientCredentials
import os
import string 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class MusicData():

    def scrape_lyrics(self, artistname, songname):
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
        elif lyrics1 == lyrics2 == None:
            print("Lyrics Not Fund")
            lyrics = None
        return lyrics


    def search_spotify(self, query):
        spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id='be5bbf6003b14fd2a2226df37d633d41', client_secret='c5550fa66cf645f0a843de3e6a775f0d'))
        results = spotify.search(q='track:' + query, type='track')

        return results

    def to_lower_case(lyrics):
        results = lyrics.lower()

    def remove_lyrics_observations():
        pass
    
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



#print(MusicData().scrape_lyrics("Metallica", "creeping death"))



# print(MusicData().search_spotify('hysteria'))
