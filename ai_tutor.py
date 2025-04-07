import streamlit as st
import os
from groq import Groq

# Set up Groq API key from Streamlit Secrets
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

client = Groq(api_key=GROQ_API_KEY)

# App title and layout
st.set_page_config(page_title="Shiksha AI - Science Doubt Solver", layout="centered")
st.title("📚 Shiksha AI – Your Science Study Buddy")
st.markdown("For Class 6–10 | Based on NCERT / Indian Boards")

# Initialize session state
if "answer" not in st.session_state:
    st.session_state.answer = ""
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "error" not in st.session_state:
    st.session_state.error = ""

# User Input Area
subject = st.selectbox("Select Subject", ["Physics", "Chemistry", "Biology"])
is_important = st.toggle("Is this for exams?", value=False)
user_question = st.text_area("Type your Science doubt/question here", height=100)

col1, col2 = st.columns(2)

# Generate Answer
if col1.button("🔍 Get Answer"):
    if not user_question.strip():
        st.warning("Please type your question.")
    else:
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="llama3-8b-8192",  # latest Groq-supported model
                    messages=[
                        {
                            "role": "system",
                            "content": f"You are a science tutor helping Class 6–10 students from India. Explain clearly in simple language based on NCERT syllabus. Subject: {subject}. Exam Important: {is_important}"
                        },
                        {
                            "role": "user",
                            "content": user_question
                        }
                    ],
                    temperature=0.7,
                    max_tokens=800,
                )
                st.session_state.answer = response.choices[0].message.content
                st.session_state.summary = ""  # Reset summary if question changes
                st.session_state.error = ""
            except Exception as e:
                st.session_state.error = f"⚠️ Something went wrong: {e}"

# Show Summary
if col2.button("📝 Show Quick Summary (TL;DR)"):
    if not st.session_state.answer:
        st.warning("Please generate an answer first.")
    else:
        with st.spinner("Summarizing..."):
            try:
                summary_response = client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=[
                        {
                            "role": "system",
                            "content": "You summarize the following answer in a very short, student-friendly TL;DR style."
                        },
                        {
                            "role": "user",
                            "content": st.session_state.answer
                        }
                    ],
                    temperature=0.5,
                    max_tokens=200,
                )
                st.session_state.summary = summary_response.choices[0].message.content
            except Exception as e:
                st.session_state.error = f"⚠️ Summary failed: {e}"

# Display Answer
if st.session_state.answer:
    st.subheader("📖 Full Answer:")
    st.markdown(st.session_state.answer)

# Display TL;DR
if st.session_state.summary:
    st.subheader("🧠 TL;DR (Quick Summary):")
    st.info(st.session_state.summary)

# Show error if any
if st.session_state.error:
    st.error(st.session_state.error)

# Footer
st.markdown("---")
st.caption("Shiksha AI is a project in progress. Built for students across India.")
