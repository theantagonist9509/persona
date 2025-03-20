from ollama import Client
import streamlit as st
import json
import os
import mysql.connector

#The client for ollama
client = Client(host='http://localhost:11434')


#Save chat logs
def save_chat(content:str):
    #The connector
    connector = mysql.connector.connect(
        host="localhost",
        user="test",
        password="password",
        database="persona"
    )
    cursor = connector.cursor() 


    query1 = "SELECT content from conversations where conversationID = %s"
    value1 = [st.session_state.conversationID,]
    cursor.execute(query1,value1)

    previous_content = str(cursor.fetchall()[0][0])
    print("PREVIOUS ",previous_content)
    final_content = previous_content+content

    query2 = "UPDATE conversations SET content = %s,processed = 0 where conversationID = %s"
    value2 = [final_content,st.session_state.conversationID]
    cursor.execute(query2,value2)
    connector.commit()
    cursor.close()
    connector.close()
    


def handle_prompt(prompt):
    # Add user message to history
    st.chat_message('user').markdown(prompt)
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    save_chat(str("\n user: "+prompt))
    # Generate and stream response
    with st.chat_message('assistant'):
        response_placeholder = st.empty()
        full_response = ''

        history = '\n'.join(
            f'{msg["role"].title()}: {msg["content"]}'
            for msg in st.session_state.messages
        )
        
        for chunk in client.generate(
            
            model='llama3.2',
            prompt=history + '\nassistant: ',
            stream=True,
            options={'temperature': 0.1}
        ):
            token = chunk.get('response', '')
            full_response += token
            response_placeholder.markdown(full_response + '▌') # Typing indicator

        response_placeholder.markdown(full_response)

    st.session_state.messages.append({'role': 'assistant', 'content': full_response})
    save_chat(str("\n assistant: "+full_response))

    st.session_state.state = 'chat'
    st.rerun()


