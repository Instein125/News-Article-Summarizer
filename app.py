import streamlit as st
from helper import *

def main():
    st.title('News Article Summarizer')

    #Input for the google api key
    api_key = st.sidebar.text_input('Enter your Google API key:', type="password")

    #Input for the article url
    article_url = st.text_input('Enter your URL of the article:')

    if api_key and article_url:
        if st.button("Summarize"):
            st.subheader('Summary', divider = 'red')
            results = getArticle(article_url=article_url, api_key=api_key)
            if results:
                st.write(f'Title: {results[1]}')
                st.write(results[0])


if __name__ == '__main__':
    main()