import streamlit as st
import openai

# Page config
st.set_page_config(page_title="AI Science Doubt Solver", page_icon="🧪")

st.title("🧪 AI Science Doubt Solver")
st.subheader("For Class 6 to 10 | CBSE & SEBA Focused")

st.markdown("Type your science question below and get a simple explanation instantly!")

# Sidebar inputs
st.sidebar.title("🎛️ Settings")
student_name = st.sidebar.text_input("👤 Your Name (optional)")
selected_class = st.sidebar.selectbox("🎯 Select Your Class", ["6", "7", "8", "9", "10"])
subject = st.sidebar.radio("📘 Choose Subject", ["Physics", "Chemistry", "Biology"])
language = st.sidebar.selectbox("🌐 Language (Coming Soon)", ["English"], disabled=True)

# Question input
user_question = st.text_area("🔍 Enter your Science Doubt or Question:")

# API Call
if st.button("💡 Solve My Doubt"):
    if user_question.strip() == "":
        st.warning("Please enter a question first.")
    else:
        with st.spinner("Thinking like a Science teacher..."):

            try:
                # Call OpenAI GPT (assuming new client method)
                from openai import OpenAI

                client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

                prompt = f"""
You are a helpful science teacher for Indian students from Class {selected_class}. Explain the following doubt in a simple, easy-to-understand way for a student of class {selected_class}, focusing only on the selected subject: {subject}.

Question: {user_question}
Give explanation in steps. End with a short summary.
"""

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                )

                answer = response.choices[0].message.content
                st.success("✅ Here's your answer:")
                st.markdown(answer)

            except Exception as e:
                st.error("⚠️ Something went wrong. Please try again later.")
                st.exception(e)

# Footer
st.markdown("---")
st.caption("Made with ❤️ for school students in India | Built using OpenAI + Streamlit")

