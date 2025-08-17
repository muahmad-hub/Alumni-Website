from .utils import calculate_score
from profiles.models import *
import heapq
from .utils import get_neighbors, Node

F_THRESHOLD = 1
ALPHA = 0.8
BETA = 0.2

# g(n) function to calculate cost from start to current user
def g_n(profile1, profile2):
    return 1 - calculate_score(profile1, profile2)

# h(n) function which is used as an estimate of cost from current user to target, but is being used as a diversity factor here
def h_n(profile1, profile2, normalized_page_ranks, alpha=ALPHA, beta=BETA):
    similarity_score = calculate_score(profile1, profile2)
    ppr_value = normalized_page_ranks[profile2]

    heuristic = ALPHA * (similarity_score) + BETA * (1-ppr_value)

    return heuristic

def f(profile1, profile2, normalized_page_ranks):
    raw_score = g_n(profile1, profile2) + h_n(profile1, profile2, normalized_page_ranks)
    # Normalizing the f(n) score
    return raw_score/2

# Returns user, NOT profile
# A* like search: finds and returns most compatible users
def a_star_search(profile, normalized_page_ranks, max_iterations=100):
    # Froniter stores nodes, NOT users
    frontier = []
    # Stores users
    explored_frontier = set()

    good_conections = set()

    start_node = Node(profile, 0)
    heapq.heappush(frontier, start_node)

    # Iteration limit is set
    for _ in range(max_iterations):
        # Breaks if no more nodes left to traverse in the frontier
        if not frontier:
            break
        current_node = heapq.heappop(frontier)
        current_profile = current_node.profile
        
        # Ignores nodes already explored
        if current_profile in explored_frontier:
            continue
        explored_frontier.add(current_profile)
        current_f = f(profile, current_profile, normalized_page_ranks)
        # Adds node to 'good_connections' if they are below the threshold (lower f(n) value means good match)
        if current_profile != profile and current_f < F_THRESHOLD:
            good_conections.add((current_profile, current_f))
        neighbors = get_neighbors(current_profile)
        for neighbor in neighbors:
            new_f = f(profile, neighbor, normalized_page_ranks)
            neighbor_node = Node(neighbor, new_f)

            heapq.heappush(frontier, neighbor_node)

    if not good_conections:
        return None
    
    # Find best user and returhn them
    best_user = None
    best_f = float("inf")
    for connection in good_conections:
        if connection[1] < best_f:
            best_user = connection[0]
            best_f = connection[1]

    return {
        "user": best_user.id, 
        "f_n_score": best_f
        }
