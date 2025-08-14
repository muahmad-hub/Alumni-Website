# Alumni Website - Technical Details
## Table of Contents
- [Key Features](#key-features)
- [Recommendation Engine](#recommendation-engine-a-personalized-pagerank)
    - [A* Search](#a-like-search)
    - [Personalized PageRank](#personalized-pagerank)
    - [Optimising the Algorithm](#optimising-the-algorithm)
- [AI-based Classifier](#ai-skill--goal-classifier-bert--svm)
- [Real-time messaging](#real-time-messaging)
## Overview
- This Alumni Website project is an intelligent alumni networking and mentorship platform built using Django, PostgreSQL, WebSockets, and AI models. It allows alumni to find and connect with their peers and mentors through skill-based categorization and personalized recommendations
- Leaving behind friends and schoolmates after graduation is a bittersweet moment. At my first school, I lost touch with many people I considered close friends once I moved countries. Everyone moved in different directions. It left me with this feeling of disconnectedness and I didn't want to experience the same thing again at my new school
- Therefore, this platform contains real-time messaging, a mentor program, and an AI-powered recommender system built using BERT embeddings, SVM classification and a custom heuristic with Personalized PageRank to not only help professional growth but also to stay connected and support one another
- I built this project independently  after completing 3 Harvard CS50 courses (CS50x, CS50 Web, CS50 AI), combining the knowledge I learnt from each course
> See my [Dev Log and Learning Journal](dev_logs.md) for detailed progress, decisions, and problem-solving along the way.
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
[See A* implementation](../alumni_website/ai/a_star_search.py)
- This isn't truly an A* search as the goal node is not known beforehand, and there is also no need for path reconstruction. However, the algorithm does use A*-like heuristics and search patterns to find the most similar alumn to the user
- A* search formula:
    - *f(n) = g(n) + h(n)*
        - *f(n)* -> total cost of reaching the most optimal alum
        - *g(n)* -> path cost calculated as 1 - similarity_score
        - *h(n)* -> this is used as a penalty for lack of diversity, calculated as ALPHA * (similarity_score) + BETA * (1-personalized_page_rank_value)
- *g(n)* This calculates a score based on how similar the users are. The more similar the a user is the lower the value of *g(n)* 
    - Similarity is calculated using the `calculate_score()` function ([see implementation at line 93](../alumni_website/ai/utils.py)) that I created which takes into account the following:
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
[See Personalized PageRank implementation here](../alumni_website/ai/personalized_page_rank.py)
- I've also implemented a personalized page rank algorithm, which serves as a sort of counter to the local nature of the A* search as it rewards nodes with higher global relevance. This allows it to suggest alumni who aren't directly related to the target user but are relevant
- The graph used has users' profiles defined as nodes and has weighted edge if users share a similar trait
- The algorithm starts off at the target user and performs a random walk throughout the graph with a bias towards the target user
- The bias means that if the algorithm has to decide which neighbor to move to it will prefer to move to the neighbor that is more relevant to the target user. It does look at other users, too but with a lower probability
- The algorithm completes when the page rank scores converge below a given threshold or when the maximum iteration limit is reached to avoid exhausting the system
- A damping factor is also used to ensure that the algorithm doesn't get stuck in a local loop as it adds a small probability that the random surfer will restart at the target user
- Once completed, each user has a Personalized PageRank score, which is a probability distribution that represents the likelihood of landing on that node from the target user. Higher-ranked nodes are more relevant to the target user
### Optimising the Algorithm
- Though the implementation of the algorithm was correct. It was computaionally naive, in the sense that there were too many redundant databse queries and no memeory optimization.
- After researching for different ways algorithms are made efficient for production and made a list of methods to improve my algorithm:
    - **Batch processing:** instead of constantly calling and looping over users and calling a specific function, I could process all the data at once
    - **Cache the data:** Instead of querying the database every time specific data is needed, it is more efficient to query the database once and then cache the data. This significantly reduces the number of queries made
    - **Memory Optimization:** Instead of storing full objects in variables, it is better to store integers or strings like IDs. Additionally, using `__slots__` when defining classes also reduces memory usage as it limits storing the data to only those attributes specified.
    - **Algorithm Pruning:** Instead of allowing the algorithm to run infinitely and exhaust the system, I should have used pruning to set a limit to how deep the algorithm goes. Furthermore, in A* search I could limit the number of users in the frontier and exit once a set number of top users below the threshold are found.
    - **Vectorization:** Using numpy for mathematical operations is highly effective as it is done under the hood in C. Numpy arrays are also contiguous (they are stored in a continuous sequence without any gaps)
> For a more detailed walkthrough of the optimization, see my [Dev Log and Learning Journal](dev_logs.md#date-august-8--9) for August 8 & 9.
## AI Skill & Goal Classifier (BERT/TF-IDF + SVM)
- Instead of comparing literal skills and goals in the recommendation engine, I decided to build a supervised learning model which will classify both of them into categories using semantic embeddings from BERT with SVM for classification
- I intially though of using an unsupervised learning model. However, using a supervised learning model would allow for better evaluation of results and allow me to define the categories
### Why BERT/TF-IDF and SVM
- BERT:
    - BERT is a transformer, which uses many self-attention heads aong with positional embeddings to get the context and semantic meaning of words in a sentence or phrase
    - I initially did think of using Bag of Words or Word2Vec; however, bag of words would be not be as accurate and Word2Vec has lower dimensions and hence can't understand words in context
    - Additionally, BERT also converts words into 768 dimensional vectors, which is very rich for the classification system to use
    - I did try using TF-IDF, expecially for skill vectorization as they are usually smaller inputs. However, the performance of the system was not up to the standard when compared with BERT
    - However, do to memory constraints in deployment (512MB for RAM) using BERT is unsuitable due to its memory usage. Instead I switched to using . More information about the integration can be found [here](dev_logs.md#tf-idf-integration-for-deployment)
- SVM:
    - SVM (Support Vector Machine) is a supervised machine learning model that classifies data by drawing boundary lines
    - SVM works well with high dimensional data like from BERT vectors
    - I compared F1 scores between three different different machine learning algorithms:
        - For Goal classification (BERT embeddings):
            - SVM (using polynomial kernel): 81.09%
            - Naive Bayes: 74.48%
            - Logistic regression: 80.21%
    - I decided to use SVM, with the polynomial kernel for goals classification, as it had the best balance of precision/recall
### Training & Performance
- I manually labbeled datasets, with ~300 fields, for both skills and goals (8 categories for skill and 5 categories for goals) 
- For goal classification acheived (using polynomial kernel and BERT embeddings):
    - Precision: 83.15%
    - Recall: 82.76%
    - F1 Score: 81.09%
- For skill classification achieved (using linear kernel and BERT embeddings):
    - Precision: 84.35%
    - Recall: 69.61%
    - F1 Score: 72.14%
- I used an 80/20 training and testing split for these results
- Skill classification used to a relatively low F1 score. It was most likely due to the fact that skill-related inputs tend to have fewer words. This makes it harder for the model to capture the context. A higher-quality dataset was needed to counter this and so I extended the dataset for skills from ~300 fields to around ~500 fields.
- In the `calculate_score()` function, I’ve assigned a lower weight to the skill overlap component so that it contributes less to the final score compared to the goal classification.
- During testing, the classifier did confuse the goal of "working in a big AI company" as an Educational goal, likely due to AI being used a lot in Educational goals.
- More training data might help differentiate similar categories better
### Integration in the app
- The model is trained and stored for effeciency using the `train_and_save_model()` function [see implementation at line 19](../alumni_website/ai/classifier.py)
- Anytime a user updates or enter a skill or goal the `predict_category_skill()` and `predict_category_goal()` are called and the skill/goal along with the category are stored in the database. [See both function here](../alumni_website/ai/classifier.py)
## Real-time Messaging 
- To allow for real-time communication between alumni, I implemented a full-duplex WebSocket-ased chat system using Django channels and currently using in-memory layer. This allows for instantaneuous and low-latency message delievery without repeated HTTP requests
### WebSockets
- HTTP is a request-response based model and so is unsuitable for real-time and bidirectional messaging as it would require the client to constantly poll the server to check if any messages have been deleivered. This would be ineffecient and cause latency
- WebSockets, however, are protocols that allow bidirectional communication between the client and server through use of a TCP connection.
- This allows for:
    - Live chat
    - Future extensibility (like live notifications)
### Consumer Logic
[See consumers.py](../alumni_website/messaging/consumers.py)
### System Architecture
<img src="docs/SA_message_app.PNG" width="700">

- As soon as the DOM is loaded, the browser's Javascript connects to a WebSocket provided by Django Channels
- This creates a bidirectional communication channel between the browser and Django channels
- When the user sends a message:
    - Javascript sends the message via the open WebSocket connection ([See implementation here](../alumni_website/static/messaging/javascript/messaging.js))
    - The message is received by user's `MessageConsumer.receive()` method on the server
    - Inside [receive()](../alumni_website/messaging/consumers.py):
        - The message is saved to the Database (PostgreSQL)
        - Send the data using memory channel to other connected Consumers
    - The `MessageConsumer.chat_message()` delivers the message. This method sends a message to Javascript through the WebSocket connection to display the message on the UI