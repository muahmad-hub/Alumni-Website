from transformers import BertTokenizer, BertModel
import numpy
import joblib
import torch
from nltk.stem import WordNetLemmatizer
from django.shortcuts import get_object_or_404
from profiles.models import Profile
from profiles.models import Connection, Profile
from django.shortcuts import get_object_or_404

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

def get_all_connections():
    all_connections = {}

    for connection in Connection.objects.all():
        if connection.profile1.id == connection.profile2.id:
            continue

        if connection.profile1.id not in all_connections:
            all_connections[connection.profile1.id] = set()
        if connection.profile2.id not in all_connections:
            all_connections[connection.profile2.id] = set()

        all_connections[connection.profile1.id].add(connection.profile2.id)
        all_connections[connection.profile2.id].add(connection.profile1.id)

    return all_connections

def calculate_score(user1, user2):
    profile1 = get_object_or_404(Profile, user = user1)
    profile2 = get_object_or_404(Profile, user = user2)

    skills_overlap = len(set(profile1.skills) & set(profile2.skills)) / len(set(profile1.skills) | set(profile2.skills))
    goals_overlap = len(set(profile1.goals) & set(profile2.goals)) / len(set(profile1.goals) | set(profile2.goals))

    university_location = 1 if profile1.university_location == profile2.university_location else 0
    location = 1 if profile1.location == profile2.location else 0

    education_level = 1 if profile1.education_level == profile2.education_level else 0

    grad_year_diff = abs(profile1.graduation_year-profile2.graduation_year)
    max_difference = 6

    graduation_year = max(0, 1 - (grad_year_diff/max_difference))

    all_connections = get_all_connections()

    mutual_connections = len(set(all_connections[profile1.profile.id]) & set(all_connections[profile2.profile.id])) / len(set(all_connections[profile1.profile.id]) | set(profile2.profile.id))

    w1, w2, w7 = 0.25
    w3, w4, w5, w6, w8 = 0.125


    score = (
        w1 * skills_overlap +  
        w2 *  goals_overlap + 
        w3 * university_location + 
        w4 * location + 
        w5 * education_level + 
        w6 * graduation_year +
        w7 * mutual_connections 
    )

    total_possible_score = w1 + w2 + w3 + w4 + w5 + w6 + w7

    if profile1.employer is not None and profile2.employer is not None:
        employer_match = 1 if profile1.employer == profile2.employer else 0
        employer = w8 * employer_match
    else:
        employer = 0

    score += employer
    total_possible_score += w8

    final_score = score/total_possible_score

    return final_score

class Node:
    def __init__(self, user, cost):
        self.user = user
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost