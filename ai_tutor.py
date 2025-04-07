import streamlit as st
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("📚 AI Study Buddy")

user_input = st.text_input("Ask me anything:")

if user_input:
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful study assistant."},
            {"role": "user", "content": user_input},
        ]
    )

    st.write(response.choices[0].message.content)
