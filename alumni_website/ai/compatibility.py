def calculate_score(user1, user2):
    skills_overlap = len(set(user1.skills) & set(user2.skills)) / len(set(user1.skills) | set(user2.skills))
    goals_overlap = len(set(user1.skills) & set(user2.skills)) / len(set(user1.skills) | set(user2.skills))

    university_location = 1 if user1.university_location == user2.university_location else 0
    location = 1 if user1.location == user2.location else 0

    education_level = 1 if user1.education_level == user2.education_level else 0

    grad_year_diff = abs(user1.graduation_year-user2.graduation_year)
    max_difference = 6

    graduation_year = max(0, 1 - (grad_year_diff/max_difference))

    score = (
        0.25 * skills_overlap +  
        0.25 *  goals_overlap + 
        0.125 * university_location + 
        0.125 * location + 
        0.125 * education_level + 
        0.125 * graduation_year
    )

    if user1.employer is not None and user2.employer is not None:
        employer_match = 1 if user1.employer == user2.employer else 0
        employer = 0.125 * employer_match
    else:
        employer = 0

    score += employer

    return score

