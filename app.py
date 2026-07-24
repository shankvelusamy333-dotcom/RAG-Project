import streamlit as st
from groq import Groq

# --------------------------------
# Page Config
# --------------------------------
st.set_page_config(
    page_title="GitHub Post Generator",
    page_icon="🚀",
    layout="wide"
)

# --------------------------------
# Groq API
# --------------------------------
groq_api_key = st.secrets.get("GROQ_API_KEY")

if not groq_api_key:
    st.error("GROQ_API_KEY not found in Streamlit Secrets.")
    st.stop()

client = Groq(api_key=groq_api_key)

# --------------------------------
# Session State
# --------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "history" not in st.session_state:
    st.session_state.history = []

# --------------------------------
# Sidebar
# --------------------------------
with st.sidebar:
    st.title("📚 History")

    if st.button("➕ New Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    if len(st.session_state.history) == 0:
        st.info("No generated content yet")

    for item in reversed(st.session_state.history):
        st.write(f"📄 {item}")

# --------------------------------
# Main Title
# --------------------------------
st.title("🚀 GitHub Post Generator")

st.markdown("""
Generate:

- GitHub Posts
- LinkedIn Posts
- README Files
- Portfolio Descriptions
- Internship Posts
- Workshop Summaries
- Project Documentation
""")

# --------------------------------
# Show Previous Messages
# --------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --------------------------------
# Chat Input
# --------------------------------
prompt = st.chat_input(
    "Describe your project..."
)

if prompt:

    # Save User Message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # System Prompt
    system_prompt = """
You are Shank Content Writer.

Create:
- GitHub Posts
- LinkedIn Posts
- README Files
- Portfolio Descriptions
- Internship Posts
- Workshop Summaries
- Project Documentation

Rules:
- Write as if Shankari Velusamy personally wrote it.
- Use first-person language.
- Use statements like:
  - I built...
  - I developed...
  - I learned...
  - One challenge I faced...
  - This project helped me...
- Never mention AI generated content.
- Never say you are an AI assistant.
- Sound natural and professional.
- Add relevant emojis.
- Do not ask questions.
- Generate complete content directly.
- Include:
  🚀 Title
  📝 Overview
  🛠 Technologies Used
  ✨ Key Features
  📚 What I Learned
  🎯 Future Improvements
- Make reasonable assumptions if details are missing.
- Content must be ready to post immediately.
"""

    with st.chat_message("assistant"):

        with st.spinner("Generating content..."):

            try:

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": system_prompt
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                answer = response.choices[0].message.content

                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

                title = prompt[:40]

                if title not in st.session_state.history:
                    st.session_state.history.append(title)

            except Exception as e:
                st.error(f"Error: {e}")