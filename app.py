import pandas as pd
import streamlit as st
import lyricsgenius as lg
import base64
import plotly.express as px
import plotly.graph_objects as go
from simpletransformers.classification import ClassificationModel
from scipy.special import softmax


def main():

    st.sidebar.title('Menu')

    # st.image('style/musicmood.png')

    application_selection = st.sidebar.selectbox('Select application', ['Home','Lyrics Analysis', "Playlist Creator"])

    if application_selection == 'Home':
        set_png_as_page_bg('music_mood_home.png')

    ## Sentiment Analysis
    if application_selection == 'Lyrics Analysis':
        st.title('Music Mood')
        #set_png_as_page_bg('musicmood.png')

        st.sidebar.title("Search Lyrics")
        song = st.sidebar.text_input('Enter song name')
        artist = st.sidebar.text_input('Enter artist name')

        ## Call lyrics api
        genius = lg.Genius(st.secrets["genius_secret"], skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"], remove_section_headers=True)

        if song is not "":
            try:
                lyrics = genius.search_song(song, artist)
                if lyrics is None:
                    st.error("Lyrics not found")
            except:
                 st.error("No lyrics found")

            if lyrics is not None:
                if st.sidebar.checkbox('Show lyrics'):
                    st.title(f"Lyrics for: {song}")
                    st.write(lyrics.lyrics) 


                if st.sidebar.checkbox("Get Music Mood"):

                    model = ClassificationModel("xlnet", "models",use_cuda=False)
                    predictions, raw_outputs = model.predict([lyrics.lyrics])
                    probabilities = softmax(raw_outputs, axis=1)
                    #st.write(probabilities)

                    st.markdown(f"O sentimento predomintante de '{song}' é ...")

                    

                    df_mood = pd.DataFrame(probabilities)
                    #df_mood =df_mood.T
                    #df_mood['song'] ='song'
                    #df_mood['name'] = ['happiness', 'passion', 'anger','sadness']
                    #st.write(df_mood)
                    plot_mood(df_mood)

                    st.markdown("""

                    Music Moods are a way of describing the emotions that are associated with music using NLP models. \n\n
                    """)

                    #for label, score in zip(mood['labels'],mood['scores']):
                    #     st.write(f"{label}: {score}")
                    #mood_dict = {k:v for k,v in zip(mood['labels'],mood['scores'])}
                    #plot_mood(mood_dict, song)


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




# def plot_mood(mood_dict, song):
#     df = pd.DataFrame([mood_dict])
#     df = df.transpose().reset_index().rename(columns={'index':'moods',0:'percentual'})

#     fig = px.pie(df, values='percentual', names='moods', title=f'Moods for {song}', color='moods',
#              color_discrete_map={'anger':'darkred',
#                                  'happiness':'green',
#                                  'sadness':'orange',
#                                  'passion':'purple'})
    # st.plotly_chart(fig)

def plot_mood(df):
    #st.write(df)
    sentiments = df.to_numpy()[0]
    fig = go.Figure(data=[
    go.Bar(name='',
           x= [''],
           y= [sentiments[0]],
           marker_color ="#85bf5e",
           hovertemplate= "Happiness: %{y:.0%}"),
    go.Bar(name='',
           x= [''],
           y= [sentiments[1]],
           marker_color = "#fec778",
           hovertemplate= "Passion: %{y:.0%}" ),
    go.Bar(name='',
           x= [''],
           y= [sentiments[2]],
            marker_color = "#e0342c",
           hovertemplate= "Anger: %{y:.0%}" ),
    go.Bar(name='',
           x= [''],
           y= [sentiments[3]],
           marker_color="#73c3ed",
           hovertemplate= "Sadness: %{y:.0%}" ),
    ])
    fig.update_layout(barmode='stack')
    fig.update_layout(showlegend=False)
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout(height=800)
    fig.update_layout(width=800)
    fig.update_layout(paper_bgcolor='#0e1118')
    fig.update_layout(plot_bgcolor='#0e1118')
    fig.add_shape(type="circle",
        xref="x", yref="y",
        x0=-0.7, y0=-0.3, x1=0.7, y1=1.3,
        line_color="#000",
        line =dict(
            width=200
        )
    )

    fig.add_shape(type="circle",
        xref="x", yref="y",
        x0=-0.5, y0=-0.1, x1=0.5, y1=1.1,
        line_color="#555",
        line =dict(
            width=2
        )
    )

    fig.add_shape(type="circle",
        xref="x", yref="y",
        x0=-0.6, y0=-0.2, x1=0.6, y1=1.2,
        line_color="#555",
        line =dict(
            width=2
        )
    )


    fig.add_shape(type="circle",
        xref="x", yref="y",
        x0=-0.7, y0=-0.3, x1=0.7, y1=1.3,
        line_color="#555",
        line =dict(
            width=2
        )
    )

    fig.add_shape(type="circle",
        xref="x", yref="y",
        x0=-0.8, y0=-0.4, x1=0.8, y1=1.4,
        line_color="#555",
        line =dict(
            width=2
        )
    )

    fig.add_shape(type="circle",
        xref="x", yref="y",
        x0=-0.9, y0=-0.5, x1=0.9, y1=1.5,
        line_color="#555",
        line =dict(
            width=2
        )
    )

    st.plotly_chart(fig)



if __name__ == '__main__':
    main()
