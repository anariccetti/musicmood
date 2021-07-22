import pandas as pd
import streamlit as st
import lyricsgenius as lg
from transformers import pipeline
import base64
import plotly.express as px


def main():
    
    st.sidebar.title('Menu')

    # st.image('style/musicmood.png')
    
    application_selection = st.sidebar.selectbox('Select application', ['Home','Lyrics Analysis', "Playlist Creator"])

    if application_selection == 'Home':
        set_png_as_page_bg('music_mood_home.png')

    ## Sentiment Analysis
    if application_selection == 'Lyrics Analysis':
        st.title('Music Mood')
        set_png_as_page_bg('musicmood.png')

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

                

            if st.sidebar.button("Get Music Mood"):

                ## Carregar modelo de sentimento
                classifier = pipeline("zero-shot-classification")
                candidate_labels = ["anger","sadness","passion","happiness"]
                hypothesis = "The emotion of this music is {}."

                mood = classifier(lyrics.lyrics, candidate_labels, hypothesis_template=hypothesis)
                
                st.markdown("""

                Music Moods are a way of describing the emotions that are associated with music using NLP models. \n\n
                """)
                
                
                # for label, score in zip(mood['labels'],mood['scores']):
                #     st.write(f"{label}: {score}")
                mood_dict = {k:v for k,v in zip(mood['labels'],mood['scores'])}
                plot_mood(mood_dict, song)
                
               

       

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

def plot_mood(mood_dict, song):
    df = pd.DataFrame([mood_dict])
    df = df.transpose().reset_index().rename(columns={'index':'moods',0:'percentual'})
    
    fig = px.pie(df, values='percentual', names='moods', title=f'Moods for {song}', color='moods',
             color_discrete_map={'anger':'darkred',
                                 'happiness':'green',
                                 'sadness':'orange',
                                 'passion':'purple'})
    st.plotly_chart(fig)
       

if __name__ == '__main__':
    main()
