# Alumni Website Project
## Overview
- This Alumni Website project is an intelligent alumni networking and mentorship platform built using Django, PostgreSQL, WebSockets, and AI models. It allows alumni to find and connect with their peers and mentors through skill-based categorization and personalized recommendations
- Leaving behind friends and schoolmates after graduation is a bittersweet moment. At my first school, I lost touch with many people I considered close friends once I moved countries. Everyone moved in different directions. It left me with this feeling of disconnectedness and I didn't want to experience the same thing again at my new school
- Therefore, this platform contains real-time messaging, a mentor program, and an AI-powered recommender system built using BERT embeddings, SVM classification and a custom heuristic with Personalized PageRank to not only help professional growth but also to stay connected and support one another
- I built this project independently  after completing 3 Harvard CS50 courses (CS50x, CS50 Web, CS50 AI), combining the knowledge I learnt from each course
## Key features
- **User profiles:** Searchable alumni and mentor database with editable user info
- **Mentorship program:** Request, accept, & allow mentors to manage requests seamlessly through their personalized dashboard
- **Dynamic Directory Search:** Name/skill + filters by university & batch year
- **Real-time chat:** WebScoket-powered messaging
- **AI Categorization:** BERT + SVM model to classify skills and goals
- **Recommendation Engine:** A*-like heuristics + Personalized PageRank
- **Tech Stack:** Django, PostgreSQL, WebSockets, HTML/CSS/JS
## Recommendation Engine (A* + Personalized PageRank)
- To connect users with relevant alumni, I developed a hybrid recommendation algorithm using graph-based scoring
### Problem structure
- The goal is to recommend the most relevant alumn to the user, while also keeping the recommendations diverse
- This was modeled as a personalized graph traversal and ranking problem, with nodes being represented as a user's profile and weighted edges representing compatibility
### A*-like search
[See A* implementation](ai/a_star_search.py)
- This isn't truly an A* search as the goal node is not known beforehand, and there is also no need for path reconstruction. However, the algorithm does use A*-like heuristics and search patterns to find the most similar alumn to the user
- A* search formula:
    - *f(n) = g(n) + h(n)*
        - *f(n)* -> total cost of reaching the most optimal alum
        - *g(n)* -> path cost calculated as 1 - similarity_score
        - *h(n)* -> this is used as a penalty for lack of diversity, calculated as ALPHA * (similarity_score) + BETA * (1-personalized_page_rank_value)
- *g(n)* This calculates a score based on how similar the users are. The more similar the a user is the lower the value of *g(n)* 
    - Similarity is calculated using the `calculate_score()` function ([see implementation at line 93](ai/utils.py)) that I created which takes into account the following:
        - Skills and goals
        - University, batch year and education level
        - Geographical location
        - Mutual connections 
        - Their job role and employer (if they have one)
- *h(n):* This is an important part of the recommendation engine as it penalizes too similar users. This is so that users are introduced to new perspectives, experiences and connections. Otherwise, the system might get too repetitive. For example, without the penalization, the system may only recommend alumni who are in the same batch or university. However, with the penalization, they could be recommended an alumni in a different country and field but with similar goals. This balance between relevance and diversity allows the system to give more intelligent recommendations
- *f(n):* A lower score means that the alumni is more relevant to the target user.
- The algorithm starts with the target user and explores their neighbors in the graph. The neighbors are calculated using the `get_neighbors()` function, which returns the graph as an adjacency list. This process repeats as the algorithm moves through neighboring nodes, expanding the search until the frontier is empty or a maximum iteration limit is reached. The search doesn't stop when it finds a single recommendation that meets the threshold, as other alumni may be more compatible. Therefore, the algorithm continues exploring to ensure it finds the best possible matches. Once the search is complete, the algorithm evaluates all the visited alumni and returns the one with the lowest *f(n)* value.
- Overall, the algorithm uses a weighted graph and a priority queue-based frontier
### Personalized PageRank
[See Personalized PageRank implementation here](ai/personalized_page_rank.py)
- I've also implemented a personalized page rank algorithm, which serves as a sort of counter to the local nature of the A* search as it rewards nodes with higher global relevance. This allows it to suggest alumni who aren't directly related to the target user but are relevant
- The graph used has users' profiles defined as nodes and has weighted edge if users share a similar trait
- The algorithm starts off at the target user and performs a random walk throughout the graph with a bias towards the target user
- The bias means that if the algorithm has to decide which neighbor to move to it will prefer to move to the neighbor that is more relevant to the target user. It does look at other users, too but with a lower probability
- The algorithm completes when the page rank scores converge below a given threshold or when the maximum iteration limit is reached to avoid exhausting the system
- A damping factor is also used to ensure that the algorithm doesn't get stuck in a local loop as it adds a small probability that the random surfer will restart at the target user
- Once completed, each user has a Personalized PageRank score, which is a probability distribution that represents the likelihood of landing on that node from the target user. Higher-ranked nodes are more relevant to the target user
