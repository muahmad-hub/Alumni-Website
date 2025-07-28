from utils import calculate_score
from profiles.models import *
import heapq
from .utils import get_neighbors, Node

F_THRESHOLD = 0.1

def g(user1, user2):
    return 1 - calculate_score(user1, user2)

def h(user1, user2):
    return -calculate_score(user1, user2)

def f(user1, user2):
    return g(user1, user2) + h(user1, user2)
    
# Returns user, NOT profile
def a_star_search(user):
    # Froniter stores nodes, NOT users
    frontier = []
    # Stores users
    explored_frontier = set()

    good_conections = set()

    start_node = Node(user, 0)
    heapq.heappush(frontier, start_node)


    while True:
        if not frontier:
            break
        current_node = heapq.heappop(frontier)
        current_user = current_node.user
        
        if current_user in explored_frontier:
            continue
        explored_frontier.add(current_user)
        current_f = f(user, current_user)
        if current_user != user and current_f < F_THRESHOLD:
            good_conections.add((current_user, current_f))
        neighbors = get_neighbors(current_user)
        for neighbor in neighbors:
            new_f = f(user, neighbor)
            neighbor_node = Node(neighbor, new_f)

            heapq.heappush(frontier, neighbor_node)

    if not good_conections:
        return None
    
    best_user = None
    best_f = float("inf")
    for connection in good_conections:
        if connection[1] < best_f:
            best_user = connection[0]
            best_f = connection[1]

    return best_user
