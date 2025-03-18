#THis program is meant to summarize the long conversations into salient points which can then be processed by the persona bot
from ollama import Client
import json
import os

client = Client(host='http://localhost:11434')

#This loop will continously run in the background
while True:
    try:
  
        folder_path = "chat_history"
        #Find all users with atleast one chat in the chat_history folder
        folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
        for f in folders:
            print("A")
            current_dir = folder_path+"/"+f
            #Find number of files in current directory
            num_files = len([f for f in os.listdir(current_dir) if os.path.isfile(os.path.join(current_dir, f))])

            print("B")
            output = "summaries/"+f+".txt"
            if not os.path.exists(output):
                with open(output, "w") as f:
                    f.write("0")  # Create an empty file
          
            #Get existing summary
            with open(output,"r") as f:
                #Number of chats processed
                try:
                    number = eval(f.readline())
                except:
                    print("POSSIBLE DATA LOSS")
                    number = 0
                #Text
                text = f.read()
            print("C")
            if(number==num_files):
                #No need to update
                continue
            elif(number>num_files):
                print("POSSIBLE DATA LOSS")
                number = num_files
    
            #Append files which have not been processed:
            prompt = [{
                        'role': 'system',
                        'content':
                        "Summarize this conversation in less than 1024 words",
                    }]
            prompt_text = ""
            print("D")
            for i in range(number,num_files):
                #Get the file
                file_name = current_dir+"/chat_log"+str(i)+".json"
           
                with open(file_name, 'r') as c:
                    new_data = json.load(c)
                    for data in new_data:
                        prompt_text+= data["role"]+data["content"]+"\n"
                prompt_text += "Original text "+text+"\n"
            prompt.append({'role':'user','content':prompt_text})
            
            print(prompt)
            print("E")
            #Generate response
            print("GENERATING NEW SUMMARY FOR ",str(f))

            full_response = " "
            prompt_string = "\n".join([msg["role"] + ": " + msg["content"] for msg in prompt])
            for chunk in client.generate(
            model='llama3.2',
            prompt= prompt_string,
            stream=True,
            options={'temperature': 0.1}
            ):
              
                token = chunk.get('response', '')
            
                full_response += token
            print("F")
            with open(output,"w") as f:
                f.write(str(num_files)+"\n")
                f.write(full_response)
                print("GENERATED SUMMARY")
                input()
            
    except Exception as e:
        print("ERROR::" ,e)
        input()