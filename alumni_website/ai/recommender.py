from .personalized_page_rank import ppr, normalize_ppr
from core.models import Users
from .a_star_search import a_star_search

from profiles.models import Profile, UserAlumniRecommendation
from .optimised_a_star_search import OptimisedAStarSearch
from django.core.cache import cache
from .utils import CACHE_TIMEOUT, CachedProfileData


def recommend(user):
    profile = user.profile

    page_ranks = ppr(profile)
    normalized_page_ranks = normalize_ppr(page_ranks)

    recommended_profile = a_star_search(profile, normalized_page_ranks)

    if recommended_profile:
        return recommended_profile
    else: 
        return None

def save_recommendation(profile_id, recommended_profile_id, compatibility_score):
    profile = Profile.objects.get(id=profile_id)
    recommended_profile = Profile.objects.get(id=recommended_profile_id)
    
    recommendation= UserAlumniRecommendation.objects.get(profile=profile)
    
    if recommendation:
        recommendation.recommended_profile = recommended_profile
        recommendation.compatibility_score = compatibility_score
        recommendation.save()
    
    return recommendation

def optimised_recommend(profile_id, use_cache=True, save_to_db=True):
    if use_cache:
        cache_key = f"recommendation_{profile_id}"
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
    
    searcher = OptimisedAStarSearch()
    result = searcher.a_star_search(profile_id)
    
    if result and save_to_db:
        save_recommendation(
            profile_id=profile_id,
            recommended_profile_id=result['user'],
            compatibility_score= 1 - result['f_n_score']
        )
    
    if use_cache and result:
        cache.set(cache_key, result, CACHE_TIMEOUT // 2)
    
    return result

def populate_cache():
    CachedProfileData.get_all_profile_data()
    CachedProfileData.get_connections_graph()