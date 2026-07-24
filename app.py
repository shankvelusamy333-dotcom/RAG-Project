import streamlit as st
import ollama

# Page Configuration
st.set_page_config(
    page_title="GitHub Post Generator",
    page_icon="🚀",
    layout="wide"
)

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar
with st.sidebar:
    st.title("📂 History")

    if st.button("➕ New Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    for i, item in enumerate(reversed(st.session_state.history)):
        st.write(f"📄 {item}")

# Main Page
st.title("🚀 GitHub Post Generator")
st.caption(
    "Create GitHub posts, README files, LinkedIn posts, portfolio descriptions, and project summaries."
)

# Display Chat Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
prompt = st.chat_input(
    "Describe your project or tell me what content you want..."
)

if prompt:

    # Show User Message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):

        with st.spinner("Generating content..."):

            response = ollama.chat(
                model="github-post-generator",   # Your Ollama model name
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            answer = response["message"]["content"]

            st.markdown(answer)

    # Save Chat
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    # Save History Title
    title = prompt[:40]

    if title not in st.session_state.history:
        st.session_state.history.append(title)

    st.rerun()