from .utils import OptimisedCompatibilityScore, OptimisedNeighborFinding, CachedProfileData
import gc
from django.core.cache import cache

class SimpleAlgorithm:    
    def __init__(self):
        self.scorer = OptimisedCompatibilityScore()
    
    def recommendation_algorithm(self, profile_id):
        from profiles.models import Profile
        
        try:
            profile_obj = Profile.objects.prefetch_related('skills', 'goals').get(id=profile_id)
        except Profile.DoesNotExist:
            print("_________________________ERROR: PROFILE ID NOT IN PROFILE_DATA_________________________")
            return None
        
        profile_data = self._profile_to_dict(profile_obj)
        
        # Load all other profiles
        other_profiles = Profile.objects.prefetch_related('skills', 'goals').exclude(id=profile_id)
        
        candidates = []
        
        # Process in small batches to manage memory
        batch_size = 50
        for i in range(0, len(other_profiles), batch_size):
            # Slicing other_profiles to get the batch
            batch = other_profiles[i:i + batch_size]
            
            for profile in batch:
                other_profile_data = self._profile_to_dict(profile)
                similarity_score = self.scorer.calculate_score(other_profile_data, profile_data)
                candidates.append((profile.id, similarity_score))
            
            # Remove batch to not use any memory
            del batch
        
        if not candidates:
            return None
        
        candidates.sort(key=lambda x: x[1], reverse=True)
        best_connection = candidates[0]
        
        # Removing to free up memory
        del candidates, other_profiles, profile_data
        gc.collect()
        
        return {
            "user": best_connection[0],
            "f_n_score": best_connection[1]
        }
    
    def _profile_to_dict(self, profile):
        return {
            'id': profile.id,
            'location': profile.location,
            'university': profile.university,
            'university_location': profile.university_location,
            'has_job': profile.has_job,
            'education_level': profile.education_level,
            'graduation_year': profile.graduation_year,
            'employer': profile.employer,
            'skills': set(skill.skill_category for skill in profile.skills.all()),
            'goals': set(goal.goal_category for goal in profile.goals.all()),
        }