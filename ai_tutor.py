import streamlit as st
import os
from groq import Groq

st.set_page_config(page_title="AI Science Doubt Solver", layout="centered")

st.title("🤖 AI Science Doubt Solver (Powered by Groq)")
st.markdown("Ask any science question and get an AI-generated answer instantly!")

# Get Groq API key
groq_api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=groq_api_key)

# Input box
user_input = st.text_input("Enter your science question here:")

if user_input:
    with st.spinner("Thinking..."):
        try:
            response = client.chat.completions.create(
                model="mixtral-8x7b-32768",  # Try also: "gemma-7b-it"
                messages=[
                    {"role": "system", "content": "You are a helpful AI science tutor."},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.7
            )
            answer = response.choices[0].message.content
            st.success("Answer:")
            st.write(answer)
        except Exception as e:
            st.error("Something went wrong!")
            st.exception(e)
