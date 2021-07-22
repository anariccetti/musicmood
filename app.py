import pandas as pd
import streamlit as st
import lyricsgenius as lg
from transformers import pipeline
import base64


def main():
    st.title('Music Mood')
    st.sidebar.title('Music Mood')

    # st.image('style/musicmood.png')
    set_png_as_page_bg('musicmood.png')
    application_selection = st.sidebar.selectbox('Select application', ['Lyrics Analysis', "Playlist Creator"])

    ## Sentiment Analysis
    if application_selection == 'Lyrics Analysis':
        
        st.sidebar.title("Search Lyrics")
        song = st.sidebar.text_input('Enter song name')
        artist = st.sidebar.text_input('Enter artist name')

        ## Call lyrics api
        genius = lg.Genius(st.secrets["genius_secret"], skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"], remove_section_headers=True)
        
        if (song and artist) is not None:
            try:
                lyrics = genius.search_song(song, artist)
            except:
                 st.error("No lyrics found")

            if st.checkbox('Show lyrics'):
                st.title(f"Lyrics for: {song}")
                st.write(lyrics.lyrics)

                

            if st.sidebar.button("Get music Mood"):
                classifier = pipeline("zero-shot-classification")
                candidate_labels = ["anger","sadness","passion","happiness"]
                hypothesis = "The emotion of this music is {}."

                mood = classifier(lyrics.lyrics, candidate_labels, hypothesis_template=hypothesis)
                
                st.markdown("""
                ## Music Moods

                Music Moods are a way of describing the emotions that are associated with music. \n\n
                The moods of the selected music are:
                """)
                
                for label, score in zip(mood['labels'],mood['scores']):
                    st.write(f"{label}: {score}")
                
               

       

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return


       

if __name__ == '__main__':
    main()
