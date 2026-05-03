import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
import pdfplumber


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error(" API Key not found! Check your .env file")
    st.stop()

client = Groq(api_key=api_key)


st.title(" AI Text Summarizer")
st.write("developed by Krishnaveni")

option = st.radio("Choose Input Type", ["Text", "PDF"])

text_input = ""

# TEXT INPUT
if option == "Text":
    text_input = st.text_area("Paste your text here")

# PDF INPUT
elif option == "PDF":
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")

    if uploaded_file:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_input += text


summary_length = st.selectbox(
    "Summary Length",
    ["Short", "Medium", "Detailed"]
)

bullet_points = st.checkbox("Bullet Point Summary")

language = st.selectbox(
    "Summary Language",
    ["English", "Hindi", "Telugu"]
)


if st.button("Summarize"):

    if not text_input.strip():
        st.warning("⚠️ Please enter text or upload a PDF")
        st.stop()


    if len(text_input) > 12000:
        st.warning("⚠️ Text too long! Trimming...")
        text_input = text_input[:12000]

    with st.spinner("⏳ Summarizing..."):

        style = "bullet points" if bullet_points else "paragraph"

        prompt = f"""
        Summarize the following text in {language}.

        Instructions:
        - Length: {summary_length}
        - Format: {style}
        - Keep important points
        - Avoid unnecessary details
        - Make it easy to understand

        Text:
        {text_input}
        """

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            summary = response.choices[0].message.content

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.stop()

 
    st.markdown(" Summary")
    st.markdown(summary)

    st.markdown(" 📄 Original Text")
    st.write(text_input[:1000])

    word_count = len(text_input.split())
    st.write(f"📊 Word Count: {word_count}")

    st.code(summary)

    st.download_button(
        label="⬇️ Download Summary",
        data=summary,
        file_name="summary.txt",
        mime="text/plain"
    )