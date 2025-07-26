# Dev Logs

## Date: July 15
### Moved Flask-based project to Django-based
- Switched the whole project from Flask to Djnago to take advantage of Django's advance features like secure auth system and scalability
- Added Django-based authentication system. Implemented login, sign up, and logout features.
- Added profile Model and linked project to PostgreSQL on local host.
- Created a profile edit feature
- Currently using a single app for all features

## Date: July 16
### Feature: Alumni Directory, Clickable cards in directory, and added sepereate profile edit page
- Users could already edit profile once they sign up. However, I thought that having an edit button next to each field would not be very aesthetic for users to view their profile and may hurt the UX. So I created a seperate edit page that is linked to the profile page through a button
- Directory provides a search bar, where users can search for alumni based on their name. This uses javascript to dynammically load all users that are queried.
- All the users that are loaded in the directory are clickable cards that takes you to the profile page when you click on them.

## Date: July 17
### Feature: Created Mentor system
- Added link in navigation to allow users to sign up to become mentor through a form
- **Decision:** Chose to prefill form with user data available for better UX as users won't need to enter same information again.
- A dashboard is made available to users once they become mentors.
- Dashboard allows users to see all their mentor requests and allows them to respond to the request by either accepting or declining it. They can also use the view button to view user's profile
- Edited directory to allow users to search by skills rather than alumni name

## Date: July 18
### Feature: Added advanced filtering
- Directory now allows users to search mentors by:
    - Skills (search bar)
    - University name (drop down)
    - Batch Year (drop down)
### Bug: Univeristy and Batch year search not working properly 
- When I would filter mentors by batch year and then wanted to filter them again by University. The results wouldn't change
### Solution:
- I hard coded if statments to see whether user is searching by skill, batch year or university and then queried accordingly. The if statments were ordered so that code that checks whether user has filtered by batch year came first and code for university came second.
- Used Q object in Django for complex querying and added all the queries into a seperate variable. Queried database only at the end. This meant that the code would first get all the queries that should be made and then make a single query to the database at the end.
- **Reflection** Avoid hard coding and test all possible filters when creating a filter feature

## Date: July 19
- **Decision:** Needed to decide whether to keep using a single app for the project or seperate out into multiple apps. 
- I decided to use seperate apps as it would allow the code to be more organised and the project to be scalabale. It would also allow to seperate different logics
- Seperated the project into 5 apps: 
    - `core`
    - `authentication`
    - `profiles`
    - `directory`
    - `mentorship`
- Added a single `template` and `static` folder. Each app had its own folder in `template` and `static`

## Date: July 20
## Goal: Add a realt-time messaging feature to allow users to communicate on the website.
### Progress
- Created a very basic message app prototype using HTML and HTMX. Its extremely simple and doesn't really have any major features. Just a start
- Plan on using Websockets and Redis
### Reflection
- This feature feels like a step up in complexity compared to the more typical CRUD stuff I’ve done so far. I’m realizing real-time systems involve way more coordination between the frontend and backend.
- Right now, I’m mostly focused on learning and understanding how real-time messaging actually works before getting into implementation. It’s a slower pace than I expected, but I think it’ll be worth it.


## Date: July 21
### What I learned
- Learned about requests and servers. HTTP follows a request-response model where the client initiates communication by sending a request to the server. If the request is valid, the server replies with a response. This model is inefficient for real-time chat because data is continuously transferred between multiple users and the server. This would require polling, where the client repeatedly sends requests to the server at set intervals.
- Using the WebSocket protocol is much more efficient for this purpose, as it supports bidirectional data transfer. It begins with a handshake process, where the client sends a request to the server, and if valid, the server responds. After this initial step, a WebSocket connection is established, allowing data to be sent to and from the server with ease.
- Channels are like mailboxes for each user. When a WebSocket connection is initiated by a user, a channel specific to that user is also created. Channels help the server route data to the correct users. Without them, the server wouldn't know where to send messages.
- The process of sending data can be synchronous (executed line by line, waiting for one line to finish before moving to the next) or asynchronous (multiple lines can run while others wait to complete). Both can be used for sending messages, but asynchronous code is much more efficient for real-time chats.
### What I did
- Extended the chat app's functionality to allow private chats between two users. 
- A unique id is generated for each private chat app which allows the chat app to be referenced through the url.
- Added a channels layer along with consumer.py and routing.py to allow the WebSocket to work
- Used Javascript to dynamically update the data (Switched from HTMX to Javascript)
- **Decision:** I initially wrote the code using a synchronous approach, but later switched to an asynchronous implementation as it proved to be significantly more efficient and better suited for handling multiple users concurrently
### Bug: Database was not allowing for more than one user to be registered in a message group
```python
class Groups(models.Model):
    group_name = models.CharField(max_length=255, unique=True)
    ...

class Members(models.Model):
    group = models.ForeignKey(
        Groups,
        related_name="members",
        default=shortuuid.uuid,
        unique=True,
        on_delete=models.CASCADE
    )
    ...
```
### Solution
- On debugging, I found out that the `group` field in the `Members` model had a `unique = True` constraint which created a one-to-one relationship instead of the many-to-one that I intended.
- I intended to ensure that a message group has a unique name so that it can be used in url routng. I mistakenly also thought that I had to add `unique = True` to the `Members` model too.
- I removed the `unique = True` constraint form the `Members` model and added it to the `group_name` field in the `Groups` model. I also added a default value of a shortuuid to ensure that the name will be unique and can be used in url routing. The short url is also more user freindly.
- **Reflection** pay attention to any messages in the terminal. The terminal did give a warning that a one-to-one relationship will be made when I made migrations
### Bug 2: First message after reload isn't rendered
-When the user sends the first message after their window reloads, the message is not rendered dynamically However for the rest of the messages, they are dynamically added.
### Solution
- I had mistakenly placed the **onmessage** WebSocket event listener inside another function. This caused an initial delay in for the message to be heard.
- Added the onmessage outside the function

## Date: July 24
### Thoughts/Ideas
- Just finished CS50's AI with Python
    - Learned about search algorithms, specifically Breadth First search and A* search
    - Explored and implemented concepts like NLP, optimization and linear programming
    - Also implemented AI's that carry out inference (I still need to internalize and fully understand them)
- Had an idea: maybe I could integrate some of what I’ve learned into my alumni website. For example, users could enter skills, and I could use NLP to categorize those skills under broader groups like Communicatio, like combining "public speaking" and "presenting projects".
- These categories could then feed into an AI-based mentor matching or alumni recommendation system, using something like A* or BFS to find the most relevant connections based on shared skills. I could even explore using inference or linear programming to build constraints into the recommendations (like making sure recommended skills belong to the same category).
### Note
- I’m still not sure whether I’ll implement this right away. It’s just an idea I’m noting down for now. I need to evaluate how efficient or realistic it would be for the site and whether I have the bandwidth to integrate it with the rest of the system.
### Feature: Add a real-time User online tracker
- **Decision:** Initially I set up another Model class called `OnlineUser`. However, it had a lot of the same information as the `Members` model. This would have caused redundancy in data and effected its normalization.
```python
class OnlineUser(models.Model):
    user = models.ForeignKey(Users, related_name="group_memberships", on_delete=models.CASCADE)
    group = models.ForeignKey(Groups, related_name="members", on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(null=True, blank=True) 

    def __str__(self):
        return f"{self.user} at {self.joined_at}"

class Members(models.Model):
    group = models.ForeignKey(Groups, related_name="members", on_delete=models.CASCADE)
    user = models.ForeignKey(Users, related_name="group_memberships", on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
```
- Therefore, I decided to add the `is_online` and `last_seen` fields to the `Members` model instead.

- Currently I'm just manually counting number of users that are online in the database but may switch to using Redis later as querying the database everytime maybe inconsistent 

### Bug 1: User Online count wouldnt update properly
- The user online count was incorrect and wouldn't show the right number of users online
### Solution
- I had set my online count to this
```python
online_count = Members.objects.filter(is_online=True).count() - 1
```
- If the other user was online and I currently opened the chat, it will still show user count as 0 because it didn't fully register that I am also online by the time the data loads on the webpage
- This code works better as it automatically excludes the current user from the count when querying
```python
online_count = Members.objects.filter(group=group, is_online=True).exclude(user=request.user).count()
```
### Bug 2: User online count doesn't update when user disconnects
- The count increments perfectly when a new user opens the chat. The data dynamically updates to the correct count quite well
- However when a user disconnects, the counter doesn't change dynmically. Only when the user reloads the page is the correct count is seen.
- The problem seems to be that the database is still not updated with the correct information, but I haven't been able to find the root cause. Might revisit this later or possibly switch to Redis for tracking.

## Date: July 24 & 25
### Feature: Created AI that categorizes a given skill into a category
- Built a skill classification system using fine-tuned SVM (Support Vector Machine) model and BERT-based vectorization.
- The AI takes a skill as an input and predicts its category. For example, it may predict **Maths** belonging to **Academic Skills** category
- Used HuggingFace Transformer for BERT embeddings
- Used scikit-learn for SVM implementation

#### Accuracy
- Train/Test split: 80/20
- Accuracy: 70.91%

- Train/Test split: 90/10
- Accuracy: 82.14%

- While the 82.14% accuracy is strong given the small dataset, I believe expanding the data could boost this significantly

### Bug 1: 3D array was being passed to SVM instead of 2D array
- SVM only works with a 2D array. However, in my code in the training part, SVM was receiving a 3D array and hence couldn't fit the data
### Solution
```python
skill_vector = np.vstack(skill_vector)
```
- Used Numpy to convert to 2D array
### Bug 2: Maths and Math were categorized into different categories
- Since the AI is not taught and trained on the meaning of words, it would incorrectly categorize **Math** and **Maths** into different categories.
### Solution:
- I chose to lemmatize words before turning them into vectors
- This way some words can be turned into their basic form which improves accuracy
```python
lemmatizer = WordNetLemmatizer()
text = lemmatizer.lemmatize(text)
```
### Optimization
- The model took too long to load because everytime I would call the `vectorize` function from `utils.py`, the `model` and `tokenizer` would be loaded. 
- To load them only the first time, I took the initialization of the `model` and `tokenizer` outside the function and created another function (`get_model_and_tokenizer`) that loads either of them if not loaded and returns them.
- Initially when loading `model` and `tokenizer`, the code is still slow. However, the `vectorize` function is significatly faster and so is the `predict_category` function.
## Reflection
- The database used for training is still not as comprehensive as I would have liked. This also affects the accuracy of the AI
- I might work on the database at a later date
### Notes for future reference
- Neural networks have three main layers: input, hidden (can be many hidden layers) and output layers
- There can be several nodes in the input layer which then connect with the hidden layer. When data is sent to the hidden layer, a weighted sum is calculated (this tells us about how much the AI focus on this specific node) and on the hidden layer an activation function is calculated (this tells us whether to forward this data to the next layer or not)
- Transformers are a type of neural network but have a few distinct features:
    - They carry out parrallel processing where each word of the sentence is processed in the neural network at the same time
    - They contain self-attention heads, which essentially allow each token to take into account other words and hence contextualize
- To be able to classify words/phrases into categories, you first need to convert the phrase into tokens 
    - BERT has its own tokenization process which adds a CLS token and SEP token at the start and end and also tokenizes words like understand differently, for example, BERT tokenizes unhappiness as "un" and "##happiness"
- These tokens are then converted into vectors for the AI to understand