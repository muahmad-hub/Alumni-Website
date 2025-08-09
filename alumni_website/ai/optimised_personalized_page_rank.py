from .utils import CACHE_TIMEOUT, CachedProfileData, OptimisedNeighborFinding
from django.core.cache import cache
import numpy as np

D = 0.85
PPR_THRESHOLD = 0.001

class OptimisedPersonalizedPageRank:    
    def __init__(self):
        self.profile_data = CachedProfileData.get_all_profile_data()
        self.neighbor_finder = OptimisedNeighborFinding()
        self.profile_ids = list(self.profile_data.keys())
        # Dictionary containing profile and their indexes
        self.id_to_index = {profile_id: i for i, profile_id in enumerate(self.profile_ids)}
    
    def ppr(self, user_profile_id, max_iterations=50):
        # Checking if PPR is already calculated and cached
        cache_key = f"ppr_{user_profile_id}"
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
        
        n = len(self.profile_ids)
        
        # Using NumPy array for page_rank for better performance
        page_rank = np.zeros(n)
        user_index = self.id_to_index[user_profile_id]
        # Personalizing it to the target user
        page_rank[user_index] = 1.0
        
        # Building transition matrix 
        transition_matrix = np.zeros((n, n))
        
        for i, profile_id in enumerate(self.profile_ids):
            neighbors = self.neighbor_finder.get_neighbors(profile_id)
            if neighbors:
                for neighbor_id in neighbors:
                    j = self.id_to_index[neighbor_id]
                    transition_matrix[j, i] = 1.0 / len(neighbors)
        
        # Personalized vector
        personalization = np.zeros(n)
        personalization[user_index] = 1.0
        
        # Updating the page ranks
        for _ in range(max_iterations):
            new_rank = (1 - D) * personalization + D * transition_matrix.dot(page_rank)
            
            # Using built in method rather than manual loop for optimization
            if np.sum(np.abs(new_rank - page_rank)) < PPR_THRESHOLD:
                break
            
            page_rank = new_rank
        
        # Converting back to dictionary
        result = {self.profile_ids[i]: page_rank[i] for i in range(n)}
        cache.set(cache_key, result, CACHE_TIMEOUT)
        return result
    
    def normalize_ppr(self, page_ranks):
        # Normalizing page ranks
        # Using built in functions are faster than manual loops and so max is used
        max_score = max(page_ranks.values()) if page_ranks.values() else 0
        dict = {}
        if max_score == 0:
            for user in page_ranks:
                dict[user] = 0
            return dict
        for user, score in page_ranks.items():
            dict[user] = score
        return dict