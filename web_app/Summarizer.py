#THis program is meant to summarize the long conversations into salient points which can then be processed by the persona bot
from ollama import Client
import mysql.connector
import time

client = Client(host='http://localhost:11434')



while True:
    #The mysql connector
    connector = mysql.connector.connect(
    host="localhost",
    user="test",
    password="password",
    database="persona"
    )
    cursor = connector.cursor()
    #Get all conversations which have not been processed
    print("RUNNING")
    query = "SELECT conversationID FROM conversations where processed = 0"
    cursor.execute(query)

    rows = cursor.fetchall()
    process_buffer = []
    for x in rows:
        process_buffer.append(x[0])
    

    #Process all the ids which have not been processed
    for i in process_buffer:
        print("PROCESSING CONVERSATION ",i)
        query = "SELECT content FROM conversations where conversationID = %s"
        values = [i,]
        cursor.execute(query,values)
      

        content = "system: Summarize this conversation in no more than 256 words. Avoid unnecessary details\n "
        content += cursor.fetchone()[0]
        
        print("GENERATING NEW SUMMARY")
        full_response = ""
        for chunk in client.generate(
            
            model='llama3.2',
            prompt=content,
            stream=True,
            options={'temperature': 0.1}
        ):
            token = chunk.get('response', '')
            full_response += token

        query = "UPDATE conversations SET summary = %s,processed = 1 where conversationID = %s"
        values = [full_response,i]
        cursor.execute(query,values)
        connector.commit()
        print("DONE")
    
    cursor.close()
    connector.close()
    time.sleep(1)
    
   