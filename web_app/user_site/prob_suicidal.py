from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tokenizer = AutoTokenizer.from_pretrained("gohjiayi/suicidal-bert")
model = AutoModelForSequenceClassification.from_pretrained("gohjiayi/suicidal-bert")

def prob_suicidal(string):
    inputs = tokenizer(string, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
        return torch.nn.functional.softmax(outputs.logits, dim=-1)[0, 1].item()

#def is_user_suicidal(state: State):
#    inference = llm.predict(f"""
#    You are an altert system in an emotional assistant chatbot.
#    Your task is to determine if the user is suicidal in the provided prompt.
#    Ouput only your inference, nothing else.
#    For example,
#    User: I'm quite frustrated by everything at the moment. Nothing seems to work out.
#    Inference: Not suicidal
#    User: I don't know if I can take this anymore.
#    Inference: Suicidal
#    User: {state.messages[-1].content}
#    Inference: 
#    """)

#    match inference:
#        case "Suicidal":
#            return True
#        case "Not suicidal":
#            return False
#        case _:
#            return is_user_suicidal_fallback(state)

#def is_user_suicidal_fallback(state):
#    return False