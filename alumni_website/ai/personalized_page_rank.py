from .utils import calculate_score, Node, get_neighbors
from profiles.models import Profile
import random

# Damping factor
d = 0.85
ppg_threshold = 0.001

def create_graph(user):
    profiles = Profile.objects.all()

    graph = {}

    for profile in profiles:
        graph[profile] = 1 if profile == user.profile else 0

    return graph

def ppr(user, max_iterations = 100):

    page_rank = create_graph(user)

    for _ in range(max_iterations):
        new_rank = {}
        for profile in page_rank.keys():
            neighbors = get_neighbors(profile.user)

            if not neighbors:
                continue

            neighbor_sum = 0
            for neighbor in neighbors:
                neighbor_sum += (page_rank[neighbor]) / len(get_neighbors(neighbor))

            new_rank[profile] = (1 - d) * (1 if profile == user.profile else 0) + d * neighbor_sum

        total_change = 0
        for node in new_rank.keys():
            total_change += abs(new_rank[node] - page_rank[node])
        page_rank = new_rank
        if total_change < ppg_threshold:
            break

    return page_rank



