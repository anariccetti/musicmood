import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyClientCredentials
import os


print()

# client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
# sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)







# items = results['artists']['items']
# if len(items) > 0:
#     artist = items[0]
#     print(artist['name'], artist['images'][0]['url'])

#function to attach lyrics onto data frame
#artist_name should be inserted as a string
# def lyrics_onto_frame(df1, artist_name):
#     for i,x in enumerate(df1['track']):
#         test = scrape_lyrics(artist_name, x)
#         df1.loc[i, 'lyrics'] = test
#     return df1


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
        spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id='', client_secret=''))
        results = spotify.search(q='track:' + query, type='track')

        return results



# print(MusicData().scrape_lyrics("Imagine dragons", "Believer"))

print(MusicData().search_spotify('hysteria'))