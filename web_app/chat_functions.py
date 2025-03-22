from langchain_community.llms.ollama import Ollama
import streamlit as st
import edge_tts
import asyncio
from datetime import datetime
import mysql.connector

#The client for ollama
llm = Ollama(model="hf.co/victunes/TherapyBeagle-11B-v2-GGUF:Q2_K",temperature=0.1)
#ollama run hf.co/victunes/TherapyBeagle-11B-v2-GGUF:Q2_K


#Generate speech
async def generate_speech(text):
    output_file = "sound_buffer/speech.mp3"
    tts = edge_tts.Communicate(text,st.session_state.voice)
    await tts.save(output_file)
    

#Save chat logs
def save_chat(role:str,content:str):
    #The connector
    connector = mysql.connector.connect(
        host="localhost",
        user="test",
        password="password",
        database="persona"
    )
    cursor = connector.cursor() 

    #Get last message ID
    cursor.execute("SELECT MAX(mID) from Messages")
    id = cursor.fetchone()

    messageID = 0
    if(id[0]==None):
        messageID = 0
    else:
        messageID = id[0]+1

    time_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #Create new conversation and user - conversation relation
    query = "INSERT INTO messages values(%s,%s,%s,%s)"
    values = [messageID,role,content,time_stamp]
    cursor.execute(query,values)
    connector.commit()

    query = "INSERT INTO conmess values(%s,%s)"
    values = [st.session_state.conversationID,messageID]
    cursor.execute(query,values)
    connector.commit()

    #Edit last accessed
    query = "UPDATE conversations SET lastInteraction = %s where cID = %s"
    values = [time_stamp,st.session_state.conversationID]
    cursor.execute(query,values)
    connector.commit()
    


def handle_prompt(prompt):
    # Add user message to history
    st.chat_message('user').markdown(prompt)
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    save_chat("user",prompt)
    # Generate and stream response
    with st.chat_message('assistant'):
        response_placeholder = st.empty()
        full_response = ''

        history = '\n'.join(
            f'{msg["role"].title()}: {msg["content"]}'
            for msg in st.session_state.messages
        )
        
        response = llm.stream(history + '\nassistant: ')
        for token in response:
            full_response += token
            response_placeholder.markdown(full_response + '▌') # Typing indicator

        response_placeholder.markdown(full_response)

    st.session_state.messages.append({'role': 'assistant', 'content': full_response})
    save_chat("assistant",full_response)


    asyncio.run(generate_speech(full_response))

    st.session_state.state = 'chat'
    st.rerun()


