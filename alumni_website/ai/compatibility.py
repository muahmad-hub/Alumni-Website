from profiles.models import Connection, Profile
from django.shortcuts import get_object_or_404

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
    goals_overlap = len(set(profile1.skills) & set(profile2.skills)) / len(set(profile1.skills) | set(profile2.skills))

    university_location = 1 if profile1.university_location == profile2.university_location else 0
    location = 1 if profile1.location == profile2.location else 0

    education_level = 1 if profile1.education_level == profile2.education_level else 0

    grad_year_diff = abs(profile1.graduation_year-profile2.graduation_year)
    max_difference = 6

    graduation_year = max(0, 1 - (grad_year_diff/max_difference))

    all_connections = get_all_connections()

    mutual_connections = len(set(all_connections[profile1.profile.id]) & set(all_connections[profile2.profile.id])) / len(set(all_connections[profile1.profile.id]) | set(profile2.skills))

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

