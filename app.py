import streamlit as st
from groq import Groq

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="GitHub Post Generator",
    page_icon="🚀",
    layout="wide"
)

# ---------------------------
# Groq Client
# ---------------------------
client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

# ---------------------------
# Session State
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------------------
# Sidebar
# ---------------------------
with st.sidebar:
    st.title("📚 History")

    if len(st.session_state.history) == 0:
        st.info("No content generated yet")

    for item in st.session_state.history:
        st.write("📄 " + item)

# ---------------------------
# Main Title
# ---------------------------
st.title("🚀 GitHub Post Generator")

st.markdown(
    "Generate GitHub posts, LinkedIn posts, README files, Portfolio descriptions and Project documentation."
)

# ---------------------------
# Display Chat Messages
# ---------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------------
# User Input
# ---------------------------
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

    # Show User Message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant Response
    with st.chat_message("assistant"):

        with st.spinner("Generating content..."):

            system_prompt = """
You are Shank Content Writer.

Generate:
- GitHub Posts
- LinkedIn Posts
- README Files
- Portfolio Descriptions
- Internship Posts
- Project Documentation

Rules:
- Write as if Shankari personally wrote it.
- Use first-person language.
- Do not ask questions.
- Generate complete content directly.
- Add relevant emojis.
- Sound professional and human.
- Include technologies, features, learnings and future improvements.
"""

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

    # Save Assistant Message
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    # Save History
    title = prompt[:40]

    if title not in st.session_state.history:
        st.session_state.history.append(title)

    st.rerun()