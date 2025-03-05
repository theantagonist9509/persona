from transformers import AutoModelForCausalLM,AutoTokenizer
import torch

model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name,torch_dtype=torch.float32,device_map="auto")

def genereate_response(prompt):
    #Adding some safeguards
    prompt += " Reply like you are giving therapy in English"

    inputs = tokenizer(prompt,return_tensors="pt").to("cpu")
    with torch.no_grad():
        output = model.generate(**inputs,max_new_tokens= 64)
    

    response = tokenizer.decode(output[0],skip_special_tokens=True)
    return response    