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

    tokens = text.split()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]    
    lemmatized_text = " ".join(lemmatized_tokens)

    tokens = tokenizer(lemmatized_text.lower(), return_tensors="pt")

    with torch.no_grad():
        outputs = model(**tokens)

    cls_embedding = outputs.last_hidden_state[:, 0, :]

    cleaned_cls_embedding = cls_embedding.numpy()

    return cleaned_cls_embedding

def save_model(model, path):
    joblib.dump(model, path)

def load_model(path):
    return joblib.load(path)

def get_neighbors(profile):
    profiles = Profile.objects.exclude(id=profile.id)

    neighbors = set()

    for other_profile in profiles:

        has_shared_location = 1 if other_profile.location == profile.location else 0
        has_shared_university = 1 if other_profile.university == profile.university else 0 
        has_shared_job = 1 if other_profile.has_job == profile.has_job else 0
        has_shared_education = 1 if other_profile.education_level == profile.education_level else 0
        has_shared_grad_year = 1 if other_profile.graduation_year == profile.graduation_year else 0

        user_skills = set(profile.skills.all())
        profile_skills = set(other_profile.skills.all())
        has_shared_skills = bool(user_skills & profile_skills)

        if (
            has_shared_location or
            has_shared_university or
            has_shared_job or
            has_shared_education or
            has_shared_grad_year or
            has_shared_skills
            ):
            neighbors.add(other_profile)

    return neighbors

def get_all_connections():

    all_connections = {}

    for profile in Profile.objects.all():
        all_connections[profile.id] = set()

    for connection in Connection.objects.all():
        if connection.profile1.id == connection.profile2.id:
            continue

        all_connections[connection.profile1.id].add(connection.profile2.id)
        all_connections[connection.profile2.id].add(connection.profile1.id)

    return all_connections

def calculate_score(profile1, profile2):

    total_skill_overlap = len(set(profile1.skills.all()) | set(profile2.skills.all()))
    skills_overlap = 0 if total_skill_overlap == 0 else len(set(profile1.skills.all()) & set(profile2.skills.all())) / total_skill_overlap

    total_goal_overlap = len(set(profile1.goals.all()) | set(profile2.goals.all()))
    goals_overlap = 0 if total_goal_overlap == 0 else len(set(profile1.goals.all()) & set(profile2.goals.all())) / total_goal_overlap

    university_location = 1 if profile1.university_location == profile2.university_location else 0
    location = 1 if profile1.location == profile2.location else 0

    education_level = 1 if profile1.education_level == profile2.education_level else 0

    grad_year1 = profile1.graduation_year if profile1.graduation_year is not None else 9999
    grad_year2 = profile2.graduation_year if profile2.graduation_year is not None else 9999

    grad_year_diff = abs(grad_year1 - grad_year2)
    max_difference = 6

    graduation_year_score = max(0, 1 - (grad_year_diff / max_difference))

    all_connections = get_all_connections()

    total_mutual_connections = len(set(all_connections[profile1.id]) | set(all_connections[profile2.id]))
    if total_mutual_connections == 0:
        mutual_connections = 0
    else:
        mutual_connections = len(set(all_connections[profile1.id]) & set(all_connections[profile2.id])) / total_mutual_connections

    w1 = 0.1
    w2 = w7 = 0.25
    w3 = w4 = w5 = w6 = w8 = 0.125


    score = (
        w1 * skills_overlap +  
        w2 *  goals_overlap + 
        w3 * university_location + 
        w4 * location + 
        w5 * education_level + 
        w6 * graduation_year_score +
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
    def __init__(self, profile, cost):
        self.profile = profile
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost