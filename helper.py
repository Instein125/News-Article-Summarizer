import streamlit as st
import requests
from newspaper import Article
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI


def initializeLLM(api_key):
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)
    return llm


def summarize(article_title, article_text, api_key):

    #preparing template for the prompt
    template = """Act as if you are a very good assistant that summarizes online article in a simple and easy language. Here is the article that you have to summarize:
    =====================
    Title: {article_title}

    Text: {article_text}
    =====================

    Summarize the given article in bullet points.
    """

    prompt = template.format(article_title=article_title, article_text=article_text)


    messages = HumanMessage(content=[
        {
            'type': 'text',
            'text': prompt,
        }
    ])


    #Setting llm
    llm = initializeLLM(api_key)
    response = llm.invoke([messages])

    return response.content



def getArticle(article_url, api_key):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }

    session = requests.Session()

    try:
        response = session.get(headers=headers, url=article_url, timeout=10)

        if response.status_code == 200:
            article = Article(article_url)
            article.download()
            article.parse()
            summary = summarize(article.title, article.text, api_key)
            return [summary, article.title]
        
        else:
            st.write(f"Failed to fetch article at {article_url}")
            return None

    except Exception as e:
        st.write(e)
        return None