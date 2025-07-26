from transformers import BertTokenizer, BertModel
import numpy
import joblib
import torch
from nltk.stem import WordNetLemmatizer

huggingface_model = "bert-base-uncased"

tokenizer = None
model = None

def get_model_and_tokenizer():
    global tokenizer, model
    if tokenizer is None:
        tokenizer = BertTokenizer.from_pretrained(huggingface_model)
    if model is None:
        model = BertModel.from_pretrained(huggingface_model)

    return model, tokenizer

def vectorize(text):
    model, tokenizer = get_model_and_tokenizer()

    lemmatizer = WordNetLemmatizer()
    text = lemmatizer.lemmatize(text)

    tokens = tokenizer(text.lower(), return_tensors="pt")

    with torch.no_grad():
        outputs = model(**tokens)

    cls_embedding = outputs.last_hidden_state[:, 0, :]

    cleaned_cls_embedding = cls_embedding.numpy()

    return cleaned_cls_embedding

def save_model(model, path):
    joblib.dump(model, path)

def load_model(path):
    return joblib.load(path)