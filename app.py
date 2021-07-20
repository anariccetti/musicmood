import pandas as pd
import streamlit as st
import lyricsgenius as lg
from transformers import pipeline

def main():
    st.title("Music Mood")

    application_selection = st.sidebar.selectbox('Select application', ['Lyrics Analysis', "Playlist Creator"])

    ## Sentiment Analysis
    if application_selection == 'Lyrics Analysis':
        song = st.sidebar.text_input('Enter song name')
        artist = st.sidebar.text_input('Enter artist name')

        ## Call lyrics api
        genius = lg.Genius(st.secrets["genius_secret"], skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"], remove_section_headers=True)
        
        if song and artist is not None:
            lyrics = genius.search_song(song, artist)
            if lyrics:
                st.title("Lyrics")
                st.write(lyrics.lyrics)

                

                if st.button("Get music Mood"):
                    classifier = pipeline("zero-shot-classification")
                    candidate_labels = ["anger","sadness","passion","happiness"]
                    hypothesis = "The emotion of this music is {}."

                    mood = classifier(lyrics.lyrics, candidate_labels, hypothesis_template=hypothesis)

                    st.write(mood)

            else:
                st.error("No lyrics found")

       

       

if __name__ == '__main__':
    main()
