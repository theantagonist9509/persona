from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tokenizer = AutoTokenizer.from_pretrained("gohjiayi/suicidal-bert")
model = AutoModelForSequenceClassification.from_pretrained("gohjiayi/suicidal-bert")

def is_suicidal(string):
    flags = [
        "end my life",
        "kill myself",
        "suicide",
        "want to die",
        "better off dead",
        "unbearable pain",
        "burden to others",
        "hate myself",
        "final farewell",
        "life is pointless",
        "death",
        "dying"
    ]
    contains_flags = bool(sum([(flag in string) for flag in flags]))
    
    if len(string.split()) <= 3:
        return contains_flags
    
    inputs = tokenizer(string, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
        return torch.nn.functional.softmax(outputs.logits, dim=-1)[0, 1].item() > 0.5