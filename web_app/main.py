import streamlit as st
from generate_response import genereate_response 

#Custom CSS Styling
st.markdown(
"""

""",unsafe_allow_html=True
)



#A nice friendly sidebar
with st.sidebar:
    st.title("Personabot")
    st.markdown("Please feel free to discuss with our helpful,interactive chatbot. Your conversations are private")

#Initialize chat history
#We remember past inputs as well
if "messages" not in st.session_state:
    st.session_state.messages = []

#Display the previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


#React to user input
if prompt:= st.chat_input("Tell me about yourself"):
    #Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    #Add it to the chat 
    st.session_state.messages.append({"role":"user","content":prompt})

    response = genereate_response(prompt)

    with st.chat_message("assistant"):
        st.markdown(response)
    #Add message to chat history
    st.session_state.messages.append({"role":"assistant","content":response})