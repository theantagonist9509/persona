import streamlit as st
from chat_functions import *
from datetime import datetime
import os
import mysql.connector

#FOR TESTING ONLY....
import random

#The connector
connector = mysql.connector.connect(
    host="localhost",
    user="test",
    password="password",
    database="persona"
    )
cursor = connector.cursor()

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


# Content header
st.title('🌿 Persona')
st.write('Talk to our therapeutic chatbot.')


# Defines UI
if 'state' not in st.session_state:
    st.session_state.state = 'init' # 'init' | 'chat' | 'gen'
#Should we generate sound
if "sound" not in st.session_state:
    st.session_state.sound = 1
#Sound of the user
if "voice" not in st.session_state:
    st.session_state.voice = "en-US-AndrewNeural"

# Sidebar with information
with st.sidebar:
    st.title('🌿 Persona')
    st.markdown('''
    ## About
    A friendly, interactive AI powered platform curated to assist students' mental well-being
    
    ## Features
    - 😊 Specially curated to address student issues
    - 🔒 Secured chats, which stay private unless you want to share them
    - 🤝 Connect with professionals for a more \'human\' touch

    _Made by Team Draco 🐉_
    ''')
  
    if st.checkbox("🔊 AUDIO",disabled=st.session_state.state == "gen"):
        st.session_state.sound = 1
    else:
        st.session_state.sound = 0

    if st.session_state.sound == 1:
        option = st.selectbox(
    "Choose an option:",
    ["en-US-AndrewNeural",
    "en-US-JennyNeural",	
    "en-US-AriaNeural",	
    "en-US-GuyNeural",	
    "en-GB-RyanNeural",
    "en-IN-NeerjaNeural",
    "en-IN-PrabhatNeural"],disabled=st.session_state.state == "gen"    
    )
        st.session_state.voice = option
        st.markdown("Changes will take effect from the next conversation")






# Useful when actiions require a UI update and then function a call (like a button click)
if 'callbacks' not in st.session_state:
    st.session_state.callbacks = []

#User details (from login)
#Query and values
if "userID" not in st.session_state:
    st.session_state.userID = random.randint(0,2)
    query = ("SELECT name from users where uID = %s")
    values = [st.session_state.userID]
    cursor.execute(query,values)
    name = cursor.fetchone()[0]
    st.session_state.name = name

# Initialize session_state
if 'messages' not in st.session_state:

    
    st.session_state.messages = [{
        'role': 'system',
        'content':
            f"The name of the user is {st.session_state.name} "
            "You are a therapeutic bot who wants to know more about the user's mental state."
            "If you believe that the student really needs help tell him/her to contact the college counselor (+91 98555 22123).Give this information if the user is really troubled or asks for this information"
            "Be as friendly as possible and ask follow up questions"
    }]

#Conversation number
if "conversationID" not in st.session_state:
    cursor.execute("SELECT MAX(cID) from conversations")
    id = cursor.fetchone()

    
    if(id[0]==None):
        st.session_state.conversationID = 0
    else:
        st.session_state.conversationID = id[0]+1

    time_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #Create new conversation and user - conversation relation
    query = "INSERT INTO conversations values(%s,%s)"
    values = [st.session_state.conversationID,time_stamp]
    cursor.execute(query,values)
    connector.commit()

    query = "INSERT INTO usercon values(%s,%s)"
    values = [st.session_state.userID,st.session_state.conversationID]
    cursor.execute(query,values)
    connector.commit()





# Display previous messages
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg['role']):
        st.markdown(msg['content'])
   


# Initial prompt suggestions TODO generate these using the llm itself
if st.session_state.state == 'init':
    buttons = {
        'Breathing Exercises':  'Give me some breathing excercises that I can use to de-stress',
        'Meditation Tricks':    'Give me some practical meditation tricks',
        'Tips to Focus':        'GIve me some practical tips to focus',
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

#Voice chat
if len(st.session_state.messages)>1 and st.session_state.state != 'gen' and st.session_state.sound == 1:
    st.audio("sound_buffer/speech.mp3", format="audio/mp3")

# Chat input
if prompt := st.chat_input('How are you feeling today?', disabled=(st.session_state.state not in ['init', 'chat'])):
    st.session_state.state = 'gen'
    st.session_state.callbacks.append(lambda: handle_prompt(prompt))
    st.rerun()

while callbacks := st.session_state.callbacks:
    callbacks.pop()()
