from .personalized_page_rank import ppr, normalize_ppr
from .simple_algorithm import SimpleAlgorithm

from profiles.models import Profile, UserAlumniRecommendation
from .optimised_a_star_search import OptimisedAStarSearch
from django.core.cache import cache
from .utils import CACHE_TIMEOUT, CachedProfileData

# Unoptimised version
def recommend(user):
    profile = user.profile

    page_ranks = ppr(profile)
    normalized_page_ranks = normalize_ppr(page_ranks)

    recommended_profile = "" #a_star_search(profile, normalized_page_ranks)

    if recommended_profile:
        return recommended_profile
    else: 
        return None

# Saves recommended user and compatibility score in the database
def save_recommendation(profile_id, recommended_profile_id, compatibility_score):
    profile = Profile.objects.get(id=profile_id)
    recommended_profile = Profile.objects.get(id=recommended_profile_id)
    
    recommendation= UserAlumniRecommendation.objects.get(profile=profile)
    
    if recommendation:
        recommendation.recommended_profile = recommended_profile
        recommendation.compatibility_score = compatibility_score
        recommendation.save()
    
    return recommendation

# Optimised version of the A* search and PPR
# Checks if user already has a recommendation in cache and returns it, else finds user and stores it in cache
# NOTE: Optimised recommend is suitable for large scale users, for smaller scale use simple_recommend()
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

# Populate cache for data used by the optimised recommender
def populate_cache():
    CachedProfileData.get_all_profile_data()
    CachedProfileData.get_connections_graph()

# Uses the simple algorithm to recommend users
# Suitable for small scale users
def simple_recommend(profile_id):
    recommender = SimpleAlgorithm()
    result = recommender.recommendation_algorithm(profile_id)
    return result