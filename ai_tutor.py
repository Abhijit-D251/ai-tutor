import streamlit as st
from groq import Groq
import os

# Load API key securely from Streamlit Secrets
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# --- App Layout ---
st.set_page_config(page_title="Shiksha AI - Science Doubt Solver", layout="centered")
st.title("📚 Shiksha AI – Your Science Study Buddy (Class 6–10)")
st.markdown("Ask your **Science doubt** below. We’ll explain it in a simple way – just like your best teacher! 🧪")

# --- Subject Selection ---
subject = st.selectbox("Choose Subject", ["Physics", "Chemistry", "Biology"], index=0)

# --- Optional Exam Importance Toggle ---
exam_toggle = st.toggle("📌 Is this important for exams?", value=False)

# --- Text Input for Doubt ---
user_question = st.text_area("✍️ Type or paste your Science question here", height=150)

# --- Ask Button ---
if st.button("Ask Shiksha AI"):
    if user_question.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking... 💡"):
            try:
                # Add contextual system message
                system_prompt = f"""
You're Shiksha AI, a helpful science tutor for Indian students of Class 6–10.
Explain concepts in simple language, step-by-step, and in a friendly tone.

Subject: {subject}
Exam Importance: {"Yes" if exam_toggle else "No"}

Instructions:
- Use simple words (age 11–16)
- Add examples or diagrams if helpful (mention them in text)
- Be short but complete
- Avoid overly technical language
"""

                # Call Groq ChatCompletion
                response = client.chat.completions.create(
                    model="mixtral-8x7b-32768",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_question},
                    ]
                )

                answer = response.choices[0].message.content
                st.success("Here's the answer 👇")
                st.markdown(answer)

                # Optional TL;DR
                if st.toggle("🔍 Show Quick Summary (TL;DR)", value=False):
                    with st.spinner("Summarizing..."):
                        summary_prompt = f"Summarize this answer in 2–3 simple lines for quick revision:\n\n{answer}"
                        summary_response = client.chat.completions.create(
                            model="mixtral-8x7b-32768",
                            messages=[
                                {"role": "system", "content": "You summarize long science answers simply for students."},
                                {"role": "user", "content": summary_prompt},
                            ]
                        )
                        st.info(summary_response.choices[0].message.content)

            except Exception as e:
                st.error(f"⚠️ Something went wrong: {str(e)}")
