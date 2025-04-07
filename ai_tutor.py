import streamlit as st
import openai

# Load API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("AI Study Buddy")
st.write("Ask me any study-related question!")

question = st.text_input("Enter your question:")

if st.button("Get Answer"):
    if question:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": question}]
            )
            st.subheader("AI Tutor's Answer:")
            st.write(response["choices"][0]["message"]["content"])
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a question!")
