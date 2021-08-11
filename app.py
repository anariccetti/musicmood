import pandas as pd
import streamlit as st
import lyricsgenius as lg
import base64
import plotly.express as px
import plotly.graph_objects as go
from simpletransformers.classification import ClassificationModel
from scipy.special import softmax
import requests
import json

def main():

    application_selection = st.sidebar.selectbox('Select application', ['Home','Search Lyrics'])

    if application_selection == 'Home':
        set_png_as_page_bg('bkgr6.png')
        st.title('')
        st.title('')

        st.title('Welcome to Music Mood!')
        st.title('🎤🎼🎹🥁🪘🎷🎺🪗🎸🪕🎻')
        st.markdown(f"Please select 'Search Lyrics' on the left menu ⬅️⬅️⬅️")
        st.markdown(f"Write a song name and artist... Our AI will return one (or more) of the main feelings below:")

        passion = '<p style="color:pink; font-size: 20px;">passion</p>'
        st.markdown(passion, unsafe_allow_html=True)

        happiness = '<p style="color:green; font-size: 20px;">happiness</p>'
        st.markdown(happiness, unsafe_allow_html=True)

        anger = '<p style="color:red; font-size: 20px;">anger</p>'
        st.markdown(anger, unsafe_allow_html=True)

        sadness = '<p style="color:blue; font-size: 20px;">sadness</p>'
        st.markdown(sadness, unsafe_allow_html=True)

    ## Sentiment Analysis
    if application_selection == 'Search Lyrics':

        st.sidebar.title("")
        st.sidebar.title("")

        st.sidebar.title("Search Lyrics")
        st.sidebar.title("")

        song = st.sidebar.text_input('Enter song name:')
        artist = st.sidebar.text_input('Enter artist name:')

        ## Call lyrics api
        genius = lg.Genius(st.secrets["genius_secret"], skip_non_songs=True, excluded_terms=["(Remix)", "(Live)", "URLCopyEmbedCopy"], remove_section_headers=True)

        if song is not "":
            try:
                lyrics = genius.search_song(song, artist)
                if lyrics is None:
                    st.error("Lyrics not found, please check spelling or try again!")
            except:
                 st.error("Lyrics not found, please check spelling or try again!")

            if lyrics is not None:
                if st.sidebar.checkbox('Show lyrics'):
                    st.title(f"{song.capitalize()} - {artist.capitalize()} (lyrics):")
                    st.write(lyrics.lyrics) 


                if st.sidebar.checkbox("Get Music Mood"):

                    url = st.secrets["url"]
                    response = requests.post(url, data=json.dumps({"lyrics": lyrics.lyrics}))
                    
                    probabilities = json.loads(response.text)['response']

                    p1, p2, p3, p4 = probabilities.replace('[','').replace(']','').split(' ')
                    
                    print(probabilities)
                    #st.write(float(p1))
                    percentages = [float(p1), float(p2), float(p3), float(p4)]
                    #st.write(percentages)

                    st.title('')
                    st.title('')

                    st.markdown(f"The main feelings of the song '{song.capitalize()}' from '{artist.capitalize()}' are...")

                    st.image("turntable_up6.png")
                    plot_mood(percentages)
                    st.image("turntable_down6.png")

                    st.markdown("""

                    Music Mood is a way of describing the emotions that are associated with song lyrics using NLP models. \n\n
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

def plot_mood(percentages):
    #st.write(df)
    #sentiments = df.to_numpy()[0]
    fig = go.Figure(data=[
    go.Bar(name='',
           x= [''],
           y= [percentages[0]],
           marker_color ="#85bf5e",
           hovertemplate= "Happiness: %{y:.0%}"),
    go.Bar(name='',
           x= [''],
           y= [percentages[1]],
           marker_color = "#ad7098",
           hovertemplate= "Passion: %{y:.0%}" ),
    go.Bar(name='',
           x= [''],
           y= [percentages[2]],
            marker_color = "#e0342c",
           hovertemplate= "Anger: %{y:.0%}" ),
    go.Bar(name='',
           x= [''],
           y= [percentages[3]],
           marker_color="#73c3ed",
           hovertemplate= "Sadness: %{y:.0%}" ),
    ])
    fig.update_layout(barmode='stack')
    fig.update_layout(showlegend=False)
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout(height=700)
    fig.update_layout(width=700)
    fig.update_layout(paper_bgcolor='#7f7f7f')
    fig.update_layout(plot_bgcolor='#7f7f7f')
    fig.add_shape(type="circle",
        xref="x", yref="y",
        x0=-0.7, y0=-0.3, x1=0.7, y1=1.3,
        line_color="#000",
        line =dict(
            width=165
        )
    )

    fig.add_shape(type="circle",
        xref="x", yref="y",
        x0=-0.5, y0=-0.1, x1=0.5, y1=1.1,
        line_color="#555",
        line =dict(
            width=1
        )
    )

    fig.add_shape(type="circle",
        xref="x", yref="y",
        x0=-0.6, y0=-0.2, x1=0.6, y1=1.2,
        line_color="#555",
        line =dict(
            width=1
        )
    )


    fig.add_shape(type="circle",
        xref="x", yref="y",
        x0=-0.7, y0=-0.3, x1=0.7, y1=1.3,
        line_color="#555",
        line =dict(
            width=1
        )
    )

    fig.add_shape(type="circle",
        xref="x", yref="y",
        x0=-0.8, y0=-0.4, x1=0.8, y1=1.4,
        line_color="#555",
        line =dict(
            width=1
        )
    )

    fig.add_shape(type="circle",
        xref="x", yref="y",
        x0=-0.9, y0=-0.5, x1=0.9, y1=1.5,
        line_color="#555",
        line =dict(
            width=1
        )
    )

    st.plotly_chart(fig)



if __name__ == '__main__':
    main()
