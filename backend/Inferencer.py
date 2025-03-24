from transformers import AutoTokenizer, AutoModelForSequenceClassification
from langchain_community.llms.ollama import Ollama
import streamlit as st
from datetime import datetime
import mysql.connector
import torch



#Ollama
llm = Ollama(model="llama3.1",temperature=0)
# Load the tokenizer and model for mental health sentiment analysis
tokenizer = AutoTokenizer.from_pretrained("tahaenesaslanturk/mental-health-classification-v0.1")
model = AutoModelForSequenceClassification.from_pretrained("tahaenesaslanturk/mental-health-classification-v0.1")


#Analyze the sentiment
#Function to check if context suggests a potential mental condition
def sentiment_present(content:str):
    prompt = "You will be given a message from a student seeking mental assistance. Reply yes if you think there is a mental or physical issue in the statement. Otherwise reply no. Only reply yes or no. user input:-  "
    prompt += content

    full_response = ""
    response = llm.stream(prompt)

    max_size = 5
    size = 0
    for token in response:
        full_response += token
        size+=1
        if(size>max_size):
            break
    #Get the first word
    token = full_response.split()[0]
    
    #Only return 0 if we are sure there is no issue
    if(token.lower()=="no"):
        return False
    else:
        return True

#Analyze the sentiment
def sentiment(content:str):
    # Encode the input text
    inputs = tokenizer(content, return_tensors="pt")

    # Perform inference
    with torch.no_grad():
        outputs = model(**inputs)

    # Get the predicted label
    predicted_label = torch.argmax(outputs.logits, dim=1).item()
    label = model.config.id2label[predicted_label]
    return label

#A function to format the prediction
def format_prediction(prediction):
    match(prediction):
        case "EDAnonymous":
            return "eating disorder"
        case "bipolarreddit":
            return "bipolar disorder"
        case "bpd":
            return "bipolar disorder"
        case "healthanxiety":
            return "anxiety"
        case "socialanxiety":
            return "anxiety"
        case "lonely":
            return "loneliness"
        case "ptsd":
            return "PTSD"
        case "suicidewatch":
            return "extreme"

        case _:
            return prediction

#A loop to check for new messages
while True:
    #The connector
    connector = mysql.connector.connect(
        host="localhost",
        user="test",
        password="password",
        database="persona"
    )
    cursor = connector.cursor() 

    query = "SELECT mID,content from messages where ISNULL(sentiment) and role = \"user\""
    cursor.execute(query)
    rows = cursor.fetchall()

    for row in rows:
        mID = row[0]
        content = row[1]

        #Check if we can find an issue
        shouldCheck = sentiment_present(content)

        #print the content
        print("Content: ",content)
        prediction = "Normal"
        if(shouldCheck):
            prediction = sentiment(content)

        prediction = format_prediction(prediction)
        #Print the prediction    
        print("Predction: ",prediction)

        #Update the row
        query = "UPDATE MESSAGES SET sentiment = %s where mID = %s"
        values = [prediction,mID]
        cursor.execute(query,values)
        connector.commit()
        
    #Close the connection
    cursor.close()
    connector.close()