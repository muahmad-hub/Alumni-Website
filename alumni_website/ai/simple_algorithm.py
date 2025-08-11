from .utils import OptimisedCompatibilityScore, OptimisedNeighborFinding, CachedProfileData

class SimpleAlgorithm:
    def __init__(self):
        self.scorer = OptimisedCompatibilityScore()
        self.neighbor_finder = OptimisedNeighborFinding()
        self.profile_data = CachedProfileData.get_all_profile_data()

    def recommendation_algorithm(self, profile_id):
        
        if profile_id not in self.profile_data:
            print("_________________________ERROR: PROFILE ID NOT IN PROFILE_DATA_________________________")
            return None
        
        profile = self.profile_data[profile_id]
        
        candidates = []

        for other_id, other_profile in self.profile_data.items():
            if other_id == profile_id:
                continue

            similarity_score = self.scorer.calculate_score(other_profile, profile)
            candidates.append((other_id, similarity_score))

        if not candidates:
            return None
        
        # Using in built functions for greater optimisation
        candidates.sort(key=lambda x: x[1], reverse=True)

        best_connection = candidates[0]

        return {
            "user": best_connection[0],
            "f_n_score": best_connection[1]
        }
