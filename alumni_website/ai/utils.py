# from transformers import BertTokenizer, BertModel
import joblib
# import torch
from profiles.models import Connection, Profile
from django.core.cache import cache
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import os
from django.conf import settings

# Classifier variables
huggingface_model = "distilbert-base-uncased"
tokenizer = None
model = None    
# Currently set to 1 hour
CACHE_TIMEOUT = 3600

# def get_model_and_tokenizer():
#     global tokenizer, model
#     try:
#         from sentence_transformers import SentenceTransformer
#         if model is None:
#             model = SentenceTransformer("all-MiniLM-L6-v2")
#         return model, None
#     except ImportError:
#         if tokenizer is None:
#             tokenizer = BertTokenizer.from_pretrained(huggingface_model)
#         if model is None:
#             model = BertModel.from_pretrained(huggingface_model)

#         return model, tokenizer


# def vectorize(text):
#     model, tokenizer = get_model_and_tokenizer()

#     # lemmatizer = WordNetLemmatizer()

#     # tokens = text.split()
#     # lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]    
#     # lemmatized_text = " ".join(lemmatized_tokens)

#     if tokenizer is None:
#         vector = model.encode([text])[0]
#     else:
#         tokens = tokenizer(text.lower(), return_tensors="pt")

#         with torch.no_grad():
#             outputs = model(**tokens)

#         vector = outputs.last_hidden_state[:, 0, :]
#         vector = vector.numpy()

#     return vector


vectorizer = None
is_fitted = False

def get_vectorizer(corpus=None):
    global vectorizer, is_fitted
    
    if vectorizer is None:
        vectorizer = TfidfVectorizer(
            stop_words='english', 
            max_features=1000,
            ngram_range=(1, 2),
            lowercase=True,
            strip_accents='ascii'
        )
        
        if corpus is not None:
            vectorizer.fit(corpus)
            is_fitted = True
        else:
            default_corpus = get_default_corpus()
            vectorizer.fit(default_corpus)
            is_fitted = True
    
    return vectorizer

def get_default_corpus():
    return [
        # Technical skills
        "python programming software development coding",
        "java object oriented programming enterprise applications",
        "javascript web development frontend backend",
        "react angular vue frontend frameworks",
        "node express backend server development",
        "sql database mysql postgresql data management",
        "machine learning artificial intelligence data science",
        "data analysis statistics python r analytics",
        "cloud computing aws azure google cloud",
        "devops docker kubernetes ci cd deployment",
        
        # Soft skills
        "project management agile scrum team leadership",
        "communication presentation public speaking",
        "problem solving critical thinking analytical",
        "teamwork collaboration cross functional teams",
        "leadership management people skills mentoring",
        "time management organization prioritization",
        "customer service client relations support",
        "sales business development revenue growth",
        "marketing digital social media campaigns",
        "finance accounting budgeting financial analysis",
        
        # Career goals
        "career advancement professional growth promotion",
        "skill development learning new technologies",
        "networking professional relationships industry connections",
        "entrepreneurship startup business venture",
        "work life balance flexible remote work",
        "mentorship teaching knowledge sharing",
        "industry expertise domain knowledge specialization",
        "management executive leadership roles",
        "consulting advisory strategic planning",
        "innovation research development cutting edge"
    ]

def vectorize(text):
    global vectorizer, is_fitted
    
    if vectorizer is None or not is_fitted:
        get_vectorizer()
    
    if not text or text.strip() == "":
        return np.zeros(vectorizer.max_features or 1000)
    
    try:
        sparse_vector = vectorizer.transform([str(text)])
        
        dense_vector = sparse_vector.toarray()[0]
        
        return dense_vector
        
    except Exception as e:
        return np.zeros(vectorizer.max_features or 1000)

def initialize_vectorizer_with_data():
    try:        
        corpus = []
        
        profiles = Profile.objects.prefetch_related('skills', 'goals').all()
        
        for profile in profiles:
            for skill in profile.skills.all():
                if hasattr(skill, 'skill_category') and skill.skill_category:
                    corpus.append(skill.skill_category)
                elif hasattr(skill, 'name') and skill.name:
                    corpus.append(skill.name)
            
            for goal in profile.goals.all():
                if hasattr(goal, 'goal_category') and goal.goal_category:
                    corpus.append(goal.goal_category)
                elif hasattr(goal, 'name') and goal.name:
                    corpus.append(goal.name)
        
        corpus = list(set([text.strip() for text in corpus if text and text.strip()]))
        
        if corpus:
            get_vectorizer(corpus)
        else:
            get_vectorizer()
            
    except Exception as e:
        get_vectorizer()

def save_vectorizer():
    global vectorizer, is_fitted
    
    if vectorizer is None or not is_fitted:
        return
    
    try:
        model_dir = os.path.join(settings.BASE_DIR, 'ai', 'models')
        os.makedirs(model_dir, exist_ok=True)
        
        vectorizer_path = os.path.join(model_dir, 'tfidf_vectorizer.pkl')
        joblib.dump(vectorizer, vectorizer_path)
        
    except Exception as e:
        print(f"Error saving vectorizer: {e}")

def load_vectorizer():
    global vectorizer, is_fitted
    
    try:
        vectorizer_path = os.path.join(settings.BASE_DIR, 'ai', 'models', 'tfidf_vectorizer.pkl')
        
        if os.path.exists(vectorizer_path):
            vectorizer = joblib.load(vectorizer_path)
            is_fitted = True
            return True
        else:
            return False
            
    except Exception as e:
        return False

def auto_initialize():
    global vectorizer, is_fitted
    
    if vectorizer is None:
        if not load_vectorizer():
            get_vectorizer()

auto_initialize()


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

class OptimisedNode:
    # __slots__ specifies the class to only have these attributes, making it use less memory
    __slots__ = ['profile_id', 'cost']
    
    def __init__(self, profile_id, cost):
        # Storing profile id instead of full profile object 
        self.profile_id = profile_id
        self.cost = cost
    
    def __lt__(self, other):
        return self.cost < other.cost

class CachedProfileData:
    # Caching data to reduce number of Database queries

    # @staticmethod allows the method to be called without creating the object     
    @staticmethod
    def get_all_profile_data():

        # The "all_profile_data" cache key is used to fetch the profile data
        cache_key = "all_profile_data"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
        
        # .prefetch_related() fetches the skills and goals alongside the profile, reduces database queries from 3 to 1
        profiles = Profile.objects.prefetch_related('skills', 'goals').all()

        print(f"PROFILES FROM CACHED PROFILES: {profiles}")
        
        profile_data = {}
        for profile in profiles:
            profile_data[profile.id] = {
                'id': profile.id,
                'location': profile.location,
                'university': profile.university,
                'university_location': profile.university_location,
                'has_job': profile.has_job,
                'education_level': profile.education_level,
                'graduation_year': profile.graduation_year,
                'employer': profile.employer,
                # Storing skills and goals categories as strings instead of storing skill and goal object to reduce memory
                'skills': set(skill.skill_category for skill in profile.skills.all()),
                'goals': set(goal.goal_category for goal in profile.goals.all()),
            }
        
        cache.set(cache_key, profile_data, 900)

        print(f"PROFILE_DATA FROM CACHE: {profile_data}")


        return profile_data
    
    @staticmethod
    def get_connections_graph():
        """Get all connections as an adjacency list (only accepted connections)"""
        cache_key = "connections_graph"
        cached_graph = cache.get(cache_key)
        
        if cached_graph:
            return cached_graph
        
        # defaultdict creates new empty set whenever a key is accessed that doesn't exist (Safer option for graphs and adjacency lists) 
        connections_graph = defaultdict(set)
        
        # .select_related() gets the two profile object and the connection object, reduces database queries from 3 to 1
        connections = Connection.objects.filter(accepted=True).select_related('profile1', 'profile2')
        
        for conn in connections:
            if conn.profile1.id != conn.profile2.id:
                connections_graph[conn.profile1.id].add(conn.profile2.id)
                connections_graph[conn.profile2.id].add(conn.profile1.id)

        # Converting to regular dict for caching
        connections_dict = dict(connections_graph)
        cache.set(cache_key, connections_dict, CACHE_TIMEOUT)
        return connections_dict

class OptimisedCompatibilityScore:    
    def __init__(self):
        self.profile_data = CachedProfileData.get_all_profile_data()
        self.connections_graph = CachedProfileData.get_connections_graph()
        self.score_cache = {}
    
    def calculate_score(self, profile1, profile2):
        total_skill_overlap = len(set(profile1["skills"]) | set(profile2["skills"]))
        skills_overlap = 0 if total_skill_overlap == 0 else len(set(profile1["skills"]) & set(profile2["skills"])) / total_skill_overlap

        total_goal_overlap = len(set(profile1["goals"]) | set(profile2["goals"]))
        goals_overlap = 0 if total_goal_overlap == 0 else len(set(profile1["goals"]) & set(profile2["goals"])) / total_goal_overlap

        university_location = 1 if profile1["university_location"] == profile2["university_location"] else 0
        location = 1 if profile1["location"] == profile2["location"] else 0

        education_level = 1 if profile1["education_level"] == profile2["education_level"] else 0

        grad_year1 = profile1["graduation_year"] if profile1["graduation_year"] is not None else 9999
        grad_year2 = profile2["graduation_year"] if profile2["graduation_year"] is not None else 9999

        grad_year_diff = abs(grad_year1 - grad_year2)
        max_difference = 6

        graduation_year_score = max(0, 1 - (grad_year_diff / max_difference))

        total_mutual_connections = set(self.connections_graph.get(profile1['id'], [])) | set(self.connections_graph.get(profile2['id'], []))
        if len(total_mutual_connections) == 0:
            mutual_connections = 0
        else:
            mutual_connections = len(set(self.connections_graph.get(profile1['id'], [])) & set(self.connections_graph.get(profile2['id'], []))) / len(total_mutual_connections)

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

        if profile1["employer"] is not None and profile2["employer"] is not None:
            employer_match = 1 if profile1.get("employer") == profile2.get("employer") else 0
            employer = w8 * employer_match
            score += employer
            total_possible_score += w8

        final_score = score / total_possible_score if total_possible_score > 0 else 0


        return final_score
    
    def calculate_score_batch(self, profile_id, neighbor_profile_ids):
        if profile_id not in self.profile_data:
            return {}
            
        profile1_data = self.profile_data[profile_id]
        scores = {}
        
        for neighbor_id in neighbor_profile_ids:
            if neighbor_id == profile_id:
                continue
            
            if neighbor_id not in self.profile_data:
                continue
                
            # Checking cache first
            # Min/Max allow for consistent cache keys
            cache_key = f"{min(profile_id, neighbor_id)}_{max(profile_id, neighbor_id)}"
            if cache_key in self.score_cache:
                scores[neighbor_id] = self.score_cache[cache_key]
                continue
            
            profile2_data = self.profile_data[neighbor_id]
            score = self.calculate_score(profile1_data, profile2_data)
            
            self.score_cache[cache_key] = score
            scores[neighbor_id] = score
        
        return scores

class OptimisedNeighborFinding:    
    def __init__(self):
        # Storing neighbor in cache to reduce database queries
        self.profile_data = CachedProfileData.get_all_profile_data()
        self.neighbor_cache = {}
    
    def get_neighbors(self, profile_id):
        profile_data = self.profile_data[profile_id]

        # Using set to ensure that neighbors are unique
        neighbors = set()
        
        for neighbor_id, neighbor_data in self.profile_data.items():
            if neighbor_id == profile_id:
                continue
            
            has_shared_location = neighbor_data["location"] == profile_data["location"]
            has_shared_university = neighbor_data["university"] == profile_data["university"]
            has_shared_job = neighbor_data["has_job"] == profile_data["has_job"]
            has_shared_education = neighbor_data["education_level"] == profile_data["education_level"]
            has_shared_grad_year = neighbor_data["graduation_year"] == profile_data["graduation_year"]
            has_shared_skills = bool(neighbor_data["skills"] & profile_data["skills"])

            if (
                has_shared_location or
                has_shared_university or
                has_shared_job or
                has_shared_education or
                has_shared_grad_year or
                has_shared_skills
            ):
                neighbors.add(neighbor_id)

        self.neighbor_cache[profile_id] = neighbors
        return neighbors