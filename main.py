import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="Fina", layout="wide")

st.title("Fina – AI Coding Assistant 💻")

# Sidebar
st.sidebar.title("Fina Tools")

mode = st.sidebar.selectbox(
    "Choose Mode",
    [
        "Code Generation",
        "Debug Code",
        "Explain Code",
        "Refactor Code"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("Fina helps you write and understand code.")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

uploaded_image = st.file_uploader(
    "Upload Code Screenshot (optional)",
    type=["png", "jpg", "jpeg"]
)

prompt = st.chat_input("Ask Fina...")

def generate_response(user_prompt, image=None):

    system_prompt = f"""
You are fina, an AI coding assistant designed to help users with programming.

Current Mode: {mode}

Rules:
- Never mention Gemini, Google, or language models.
- If asked who created you say:
  "I am Fina, your AI coding assistant."

Mode Behavior:

Code Generation:
Write clean code with comments.

Debug Code:
Find errors and explain fixes.

Explain Code:
Explain simply with examples.

Refactor Code:
Improve code quality and performance.
"""

    contents = [user_prompt]

    if image:
        contents = [Image.open(image), user_prompt]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt
        ),
        contents=contents
    )

    return response.text


if prompt:

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Fina thinking... 💻"):

            reply = generate_response(prompt, uploaded_image)

            st.markdown(reply)

            st.session_state.messages.append(
                {"role": "assistant", "content": reply}
            )