import streamlit as st

from auth import *
from chat import *
from sidebar import *

# Configure page
st.set_page_config(
    page_title='Persona',
    layout='centered',
    page_icon='🌿',
)

# Set style
st.markdown(
    '''
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
    ''',
    unsafe_allow_html=True
)




# Defines UI
if 'state' not in st.session_state:
    st.session_state.state = 'sign-in' # 'sign-in' | 'sign-up' | 'init' | 'chat' | 'gen'

#Should we generate sound
if "sound" not in st.session_state:
    st.session_state.sound = 1

#Sound of the user
if "voice" not in st.session_state:
    st.session_state.voice = "en-US-AndrewNeural"

# Useful when actiions require a UI update and then function a call (like a button click)
if 'callbacks' not in st.session_state:
    st.session_state.callbacks = []



sidebar_ui()

if st.session_state.state == 'sign-up':
    sign_up_ui()
elif st.session_state.state == 'sign-in':
    sign_in_ui()
else:
    st.title(f"🌿 What's up, {st.session_state.user['name'].split()[0]}?")
    st.text("") # Vertical spacing
    
 
    if st.session_state.state == 'init':
        buttons = {
            'Tips for Anxiety':     'Give me practical tips to deal with anxiety.',
            'Issues with Sleeping': 'Give me practical advice on improving my sleep quality and sleep schedule.',
            'Eating Disorders':     'Tell me about eating disorders and how to tackle them.',
        }
    
        cols = st.columns([2] * len(buttons.keys()))
        button_rets = []
        
        for col, text in zip(cols, buttons.keys()):
            with col:
                button_rets.append(st.button(text))
        
        for button_ret, prompt in zip(button_rets, buttons.values()):
            if button_ret:
                st.session_state.state = 'gen'
                st.session_state.callbacks.append(lambda: handle_prompt(prompt))
                st.rerun()
    
    # Display previous messages
    if 'messages' not in st.session_state:
        st.session_state.messages = [SystemMessage(content=f"""
        You are a therapeutic bot who wants to know more about the user's mental state.
        If you believe that the user needs serious help, tell them to contact the college counselor (+91 98555 22123).
        Give this information if the user is really troubled or asks for this information.
        Be as friendly as possible and ask follow up questions.
        The name of the user is {st.session_state.user['name']}.
        """)]
    for msg in st.session_state.messages[1:]:
        role = "user" if isinstance(msg, HumanMessage) else "assistant"
        with st.chat_message(role):
            st.markdown(msg.content)
            
    if st.session_state.state == 'chat' and st.session_state.sound == 1:
        st.audio(f"user-tts/{st.session_state.user['uID']}.mp3", format="audio/mp3")
    
    # Chat input
    if prompt := st.chat_input('How are you feeling today?', disabled=(st.session_state.state not in ['init', 'chat'])):
        st.session_state.state = 'gen'
        st.session_state.callbacks.append(lambda: handle_prompt(prompt))
        st.rerun()

# Useful when actiions require a UI update and then a function call (like a button click)
if 'callbacks' not in st.session_state:
    st.session_state.callbacks = []
while callbacks := st.session_state.callbacks:
    callbacks.pop(0)()
