import streamlit as st
from functions import *

#Page configuration
st.set_page_config(
    page_title="PERSONA",
    layout="centered",
    page_icon="🌿"
)


#Session variables
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role":"ai","content":"Hey there, I am here to help"})

#Are we processing input
if "processing" not in st.session_state:
    st.session_state.processing = False



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
            font-size: 16px;
        }
        .stButton>button:hover {
            background-color: #ffeeb9 !important;
        }

    </style>
    """,
    unsafe_allow_html=True
)

def generate_history(messages):
    history = []
    for message in messages:
        history.append((message["role"],message["content"]))
    return history





#Header
st.title("🌿 PERSONA")
st.write("Talk to our helpful bot")

#A nice friendly sidebar
with st.sidebar:
    st.title("ABOUT PERSONA")
    st.markdown("A friendly,interactive AI powered platform curated to assist students.")
    st.markdown("**Features**")
    st.markdown("😊 Specially curated to address student issues")
    st.markdown("🔒 Secured chats, which stay private unless you want to share them")
    st.markdown("🤝 Connect with professionals for a more \"human\" touch")
    st.markdown("\n\n **Made by Team Draco** 🙏")

#Display the previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#Print helpful prompts if its the first message
_,col1,_, col2,_, col3,_, = st.columns([0.25,2,0.25,2,0.25,2,0.25])
if(len(st.session_state.messages)==1):
    
    with col1:
        breathing = st.button("Breathing Exercises")
    with col2:
        meditate = st.button("Meditation Tricks")
    with col3:
        focus = st.button("Tips to Focus") 

    if(breathing):
        add_prompt("Give some breathing excercises which I can use to de-stress")
    
    if(meditate):
        add_prompt("Give some meditation tricks")
    
    if(focus):
        add_prompt("Give some scientific ways to improve my focus")


user_input = st.chat_input("Tell me how you feel",disabled=st.session_state.processing)

#React to user input
if user_input and not st.session_state.processing:
    add_prompt(user_input)


#Generate response
if st.session_state.processing:

    history = generate_history(st.session_state.messages)
    
    #Generate using last message and the history
    response = genereate_response(st.session_state.messages[-1]["content"],history)


    with st.chat_message("assistant"):
        st.markdown(response)
    #Add message to chat history
    st.session_state.messages.append({"role":"ai","content":response})
    st.session_state.processing = False
    st.rerun()


