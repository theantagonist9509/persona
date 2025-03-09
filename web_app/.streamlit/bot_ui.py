import streamlit as st

st.set_page_config(
    page_title="PERSONA",
    layout="centered",
    page_icon="🌿"
)

st.markdown(
    """
    <style>
        body {
            background-color: #fffaef;
            color: #5a5a5a;
            font-family: serif;
        }
        .stApp {
            background-color: #fffaef;
        }
        h1, h2, h3, h4, h5, h6, p, label {
            color: #5a5a5a !important;
        }
        .stTextInput>div>div>input {
            background-color: #fff6db !important;
            color: black !important;
            border-radius: 10px;
            padding: 10px;
        }
        .stButton>button {
            background-color: #fff6db !important;
            color: black !important;
            border-radius: 10px;
            padding: 8px 16px;
            font-size: 16px;
        }
        .stButton>button:hover {
            background-color: #ffeeb9 !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌿 PERSONA")
st.write("Chat with the bot below:")

user_input = st.text_input("Type your message:", "")

if st.button("Send"):
    st.write(f"🤖 Chatbot: [Bot response will go here]")

st.write("---")
st.write("✨ Need extra support? Try these:")

col1, col2, col3 = st.columns(3)

with col1:
    st.button("Breathing Exercise")
with col2:
    st.button("Mindfulness Meditation")
with col3:
    st.button("Journal Your Thoughts")
