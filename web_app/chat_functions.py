from ollama import Client
import streamlit as st
import json
import os

client = Client(host='http://localhost:11434')

def handle_prompt(prompt):
    # Add user message to history
    st.chat_message('user').markdown(prompt)
    st.session_state.messages.append({'role': 'user', 'content': prompt})

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

    st.session_state.state = 'chat'
    st.rerun()


#Save chat logs
def save_chat(history,destination):
    # Create the file if it does not exist
    if not os.path.exists(destination):
        with open(destination, "w") as f:
            f.write("")  # Create an empty file
    with open(destination,"w") as f:
        json.dump(history,f)