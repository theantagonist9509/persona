from langchain_ollama import ChatOllama

llm = ChatOllama(
    model = "llama3.1",
    temperature = 0
)



def genereate_response(prompt,history):
    messages = [
        (
            "system",
            "You are a therapeutic bot who wants to know more about the patient's mental state"
        ),  
      
        
    ]
    #Add chat history
    messages.extend(history)
    #Add current prompt
    messages.append(("user",prompt))

    msg = llm.invoke(messages)
    return msg.content