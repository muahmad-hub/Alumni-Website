from .utils import get_neighbors
from profiles.models import Profile

# Damping factor
d = 0.85
ppg_threshold = 0.001

def create_graph(user_profile):
    profiles = Profile.objects.all()

    graph = {}

    for profile in profiles:
        graph[profile] = 1 if profile == user_profile else 0

    return graph

def ppr(user_profile, max_iterations = 100):

    page_rank = create_graph(user_profile)

    all_neighbors = {p: get_neighbors(p) for p in page_rank}


    for _ in range(max_iterations):
        new_rank = {}
        for profile in page_rank.keys():
            neighbors = get_neighbors(profile)

            if not neighbors:
                continue

            neighbor_sum = 0
            for neighbor in neighbors:
                 neighbor_sum += page_rank[neighbor] / len(all_neighbors[neighbor] or [1]) 

            new_rank[profile] = (1 - d) * (1 if profile == user_profile else 0) + d * neighbor_sum

        total_change = 0
        for node in new_rank.keys():
            total_change += abs(new_rank[node] - page_rank[node])
        page_rank = new_rank
        if total_change < ppg_threshold:
            break

    return page_rank

def normalize_ppr(page_ranks):
    highest = -float("inf")
    for page_rank in page_ranks.values():
        if page_rank > highest:
            highest = page_rank

    if highest == 0:
        normalized = {user: 0 for user in page_ranks}
        return normalized

    normalized = {user: score/highest for user, score in page_ranks.items()}
    return normalized
