import streamlit as st
import codecs
import streamlit.components.v1 as stc

def st_home(home_html, width=700,height=500):
    home_file = codecs.open(home_html,'r')
    page = home_file.read()
    stc.html(page, width=width,height=height,scrolling=True)

def main():
    st_home('home.html')

if __name__ =='__main__':
    main()
