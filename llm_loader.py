from langchain_community.chat_models import ChatOpenAI
import os
import streamlit as st

def get_llm():
    together_api_key = st.secrets["TOGETHER_API_KEY"]  # match this to your secrets.toml

    # Set environment variables for Together AI
    os.environ["OPENAI_API_KEY"] = together_api_key
    os.environ["OPENAI_BASE_URL"] = "https://api.together.xyz/v1"

    return ChatOpenAI(
        model="mistralai/Mixtral-8x7B-Instruct",
        temperature=0.7,
        max_tokens=1024
    )
