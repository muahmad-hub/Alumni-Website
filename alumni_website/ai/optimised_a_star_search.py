from .utils import OptimisedCompatibilityScore, OptimisedNeighborFinding, OptimisedNode
from .optimised_personalized_page_rank import OptimisedPersonalizedPageRank
import heapq

F_THRESHOLD = 1
ALPHA = 0.8
BETA = 0.2

class OptimisedAStarSearch:    
    def __init__(self):
        self.scorer = OptimisedCompatibilityScore()
        self.neighbor_finder = OptimisedNeighborFinding()
        self.ppr_computer = OptimisedPersonalizedPageRank()
    
    def g_n(self, profile_id1, profile_id2):
        scores = self.scorer.calculate_score_batch(profile_id1, [profile_id2])
        if profile_id2 not in scores:
            return 1.0
        g_n = 1 - scores[profile_id2]
        return g_n
    
    def h_n(self, profile_id1, profile_id2, normalized_page_ranks):
        scores = self.scorer.calculate_score_batch(profile_id1, [profile_id2])
        if profile_id2 not in scores:
            return 1.0

        similarity_score = scores[profile_id2]
        ppr_value = normalized_page_ranks.get(profile_id2, 0)
        h_n = ALPHA * similarity_score + BETA * (1 - ppr_value)
        return h_n
    
    def f_n(self, profile_id1, profile_id2, normalized_page_ranks):
        g_n = self.g_n(profile_id1, profile_id2)
        h_n = self.h_n(profile_id1, profile_id2, normalized_page_ranks)
        f_n = (g_n + h_n) / 2
        return f_n
    
    def a_star_search(self, profile_id, max_iterations=50, beam_width=100):
        if profile_id not in self.scorer.profile_data:
            print(f"Profile with ID {profile_id} not found in cached data")
            print(f"This is all of the data {self.scorer.profile_data}")
            print(f"The current profile id is {profile_id}")
            return None
        
        # Computing and storing page ranks only once for effeciency
        page_ranks = self.ppr_computer.ppr(profile_id)
        normalized_page_ranks = self.ppr_computer.normalize_ppr(page_ranks)
        
        frontier = []
        explored = set()
        good_connections = []
        
        start_node = OptimisedNode(profile_id, 0)
        heapq.heappush(frontier, start_node)
        
        for iteration in range(max_iterations):
            if not frontier:
                break
            
            # Beam search implementation. Keeps only top 'beam_width' in frontier, preventing frontier expanding infinitely
            if len(frontier) > beam_width:
                frontier = heapq.nsmallest(beam_width, frontier)
                heapq.heapify(frontier)
            
            current_node = heapq.heappop(frontier)
            current_profile_id = current_node.profile_id
            
            if current_profile_id in explored:
                continue
            
            explored.add(current_profile_id)
            
            current_f = self.f_n(profile_id, current_profile_id, normalized_page_ranks)
            
            if current_profile_id != profile_id and current_f < F_THRESHOLD:
                good_connections.append((current_profile_id, current_f))
            
            # Early termination if 10 good connections found, preventing over exhausting the system
            if len(good_connections) >= 10:
                break
            
            neighbors = self.neighbor_finder.get_neighbors(current_profile_id)
            
            # Batch calculation of f_n score for all neighbors
            neighbor_scores = {}
            if neighbors:
                scores = self.scorer.calculate_score_batch(profile_id, list(neighbors))
                for neighbor_id in neighbors:
                    if neighbor_id not in explored and neighbor_id in scores:
                        # I'm not calculating the actual f(n) scores for neighbors and am only using an approximation for effeciency
                        similarity = scores[neighbor_id]
                        ppr_val = normalized_page_ranks.get(neighbor_id, 0)
                        f_score = (1 - similarity + ALPHA * similarity + BETA * (1 - ppr_val)) / 2
                        neighbor_scores[neighbor_id] = f_score
            
            # Adding only top 20 most promising neighbors to frontier
            sorted_neighbors = sorted(neighbor_scores.items(), key=lambda x: x[1])[:20]
            for neighbor_id, f_score in sorted_neighbors:
                neighbor_node = OptimisedNode(neighbor_id, f_score)
                heapq.heappush(frontier, neighbor_node)
        
        if not good_connections:
            return None
        
        # good_connections is in format (profile_id, f(n) score), x[1] is used to compare the f(n) score 
        best_connection = min(good_connections, key=lambda x: x[1])
        return {
            "user": best_connection[0],
            "f_n_score": best_connection[1]
        }