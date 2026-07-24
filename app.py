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
# Groq API Setup
# --------------------------------
groq_api_key = st.secrets.get("GROQ_API_KEY")

if not groq_api_key:
    st.error("🔑 GROQ_API_KEY not found in Streamlit Secrets. Please configure it in app settings.")
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

    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    if not st.session_state.history:
        st.info("No generated content yet")
    else:
        for idx, item in enumerate(reversed(st.session_state.history)):
            st.markdown(f"📄 **{item}**")

# --------------------------------
# Main Title & Description
# --------------------------------
st.title("🚀 GitHub Post Generator")

st.markdown("""
Generate ready-to-post content:
* **GitHub & LinkedIn Posts**
* **README Files & Project Documentation**
* **Portfolio Descriptions & Internship Summaries**
""")

# --------------------------------
# Show Previous Messages
# --------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --------------------------------
# Chat Input & Logic
# --------------------------------
prompt = st.chat_input("Describe your project...")

if prompt:
    # Save User Message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # System Persona Rules
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
                # Build complete conversation payload
                api_messages = [{"role": "system", "content": system_prompt}]
                
                for msg in st.session_state.messages:
                    api_messages.append({"role": msg["role"], "content": msg["content"]})

                # Call Groq API
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=api_messages,
                    temperature=0.7,
                    max_tokens=2048,
                )

                answer = response.choices[0].message.content

                # Display generated answer
                st.markdown(answer)

                # Save Assistant Message
                st.session_state.messages.append({"role": "assistant", "content": answer})

                # Track History Snippet
                title_snippet = prompt[:35] + ("..." if len(prompt) > 35 else "")
                if title_snippet not in st.session_state.history:
                    st.session_state.history.append(title_snippet)

            except Exception as e:
                st.error(f"Error calling Groq API: {e}")