from .personalized_page_rank import ppr, normalize_ppr
from core.models import Users
from .a_star_search import a_star_search

def recommend(user):
    profile = user.profile

    page_ranks = ppr(profile)
    normalized_page_ranks = normalize_ppr(page_ranks)

    recommended_profile = a_star_search(profile, normalized_page_ranks)

    if recommended_profile:
        return recommended_profile
    else: 
        return None

