import streamlit as st
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model = "llama3.1",
    temperature = 0.1
)



def genereate_response(prompt,history):
    messages = [
        (
            "system",
            "You are a therapeutic bot who wants to know more about the patient's mental state. "
            "If you believe that the student needs help tell him/her to contact the college counselor (9855522123)"
            "Be as freindly as possible"
        ),  
      
        
    ]
    #Add chat history
    messages.extend(history)
    #Add current prompt
    messages.append(("user",prompt))

    msg = llm.invoke(messages)
    return msg.content

#A function to add a prompt
def add_prompt(prompt):
    #Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    #Add it to the chat 
    st.session_state.messages.append({"role":"user","content":prompt})
    st.session_state.processing = True
    #Rerun so that all the variables are set
    st.rerun()