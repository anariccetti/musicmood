import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyClientCredentials
import os


class MusicData():

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
        spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id='', client_secret=''))
        results = spotify.search(q='track:' + query, type='track')

        return results

    def to_lower_case():
        pass 

    def remove_lyrics_observations():
        pass
    
    def remove_punctuation():
        pass

    def remove_stop_words():
        pass
    
    def get_clean_song(self,artistname, songname):
        lyrics = self.scrape_lyrics(artistname, songname)

        lyrics = self.remove_lyrics_observations(lyrics)

        lyrics = self.remove_punctuation(lyrics)

        lyrics = self.remove_stop_words(lyrics)

        return lyrics

# print(MusicData().scrape_lyrics("the beatles", "HERE COMES THE SUN"))

# print(MusicData().search_spotify('hysteria'))