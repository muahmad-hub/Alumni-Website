from transformers import BertTokenizer, BertModel
import numpy
import joblib
import torch
from nltk.stem import WordNetLemmatizer
from django.shortcuts import get_object_or_404
from profiles.models import Profile

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

def get_neighbors(user):
    user_profile = get_object_or_404(Profile, user = user)
    profiles = Profile.objects.all()

    neighbors = set()

    for profile in profiles:
        if profile == user_profile:
            continue

        has_shared_location = 1 if profile.location == user_profile.location else 0
        has_shared_university = 1 if profile.university == user_profile.university else 0 
        has_shared_job = 1 if profile.has_job == user_profile.has_job else 0
        has_shared_education = 1 if profile.education_level == user_profile.education_level else 0
        has_shared_grad_year = 1 if profile.graduation_year == user_profile.graduation_year else 0

        user_skills = set(user_profile.skills.all())
        profile_skills = set(profile.skills.all())
        has_shared_skills = bool(user_skills & profile_skills)

        if (
            has_shared_location or
            has_shared_university or
            has_shared_job or
            has_shared_education or
            has_shared_grad_year or
            has_shared_skills
            ):
            neighbors.add(profile.user)

    return neighbors