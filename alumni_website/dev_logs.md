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

## Date: July 25 & 26
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
### Reflection
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

## Date: July 27
### What I did
- Users can now add their skills and goals on their profile page
- Added `Skills` and `Goals` model which link to the `Profile` model
- The function `predict_category_skill` and `predict_category_goal` are called to categorize and store the category in the database
- I also started working on the connection recommendation system and plan to use A* search
- Edited the classification system to allow classifying user goals as well. For example, users can say they wish to become a project manager in the tech industry which would be classified as a Career goal.
#### Accuracy of goal classification
- Train/Test split: 80/20
- Accuracy: 83.76%

- Train/Test split: 90/10
- Accuracy: 86.21%

- The goal classification system is much more accurate than the skill classification system. This could possibly be because the inputs are much larger, which reduces the room for error when classifying
### Bug: Failed WebSocket connection
- WebSocket connection was not being made when I ran the server
- The terminal was saying that the app was running on development server rather than the ASGI server
### Solution
- I had installed channels version 3.0.1, which is the older version and not compatible with the Django 5.2.4
- This meant that the app wasn't running as an ASGI application
### Note
- Make sure to check `requirements.txt` so that all the dependencies are of the latest version
### Reflection
- Since a lot of the features are now being developed, the website does feel a bit cluttered, especially the profile page.
- I might need to take a day out and work on the UI and UX 

## Date: July 28
### Features: Added A* inspired search and Personalized Page Rank search for the recommendation system
- Implemented a modified A* search algorithm that finds the topmost relevant alumni to a specific user and then returns the most relevant out of them.
- Each User is treated as a node and edges are weighted based on a custom similarity function that takes the following into account:
    - Skills
    - Goals
    - University Location
    - Current Location
    - Education Level
    - Graduation Year
    - Employer (if any)
    - Mutual Connections
- Unlike traditional A* search that has a goal node and traces back the path once the goal node is reached, this modified A* search finds the most relevant users by minimizing cost.
- I defined `g(n)` as 1 - similarity and `h(n)` as -similarity
- So if two users are similar, `g(n)` function will be minimised and so will `h(n)`. Therefore, minimising `f(n)`, which is the total cost function.
- The lower the `f(n)` function, the more similar the users are
- I also normalized the f(n) to ensure it is a value from 0 to 1 and assigned variables for the weights so it is easier to change them later on in the `calculate_score` function
- To allow for a more advance and accurate recommendation system, I implemented a Personalized Page Rank algorithm, which will be used in the heuristics of the A* search to create a hybrid system
- The page rank function will return a dictionary where the keys are users and the value is their Page Rank
### Notes for future reference
- heapq, specifically min-heap, is really beneficial for A* algorithm as it allows you to remove the smallest element effeciently because it has o(log n) time complexity compared to O(nlog n) time complexity of a list
- A* search follows this basic cost function:
    - f(n) = g(n) + h(n)
        - f(n) is the total cost function
        - g(n) is the cost of going from start node to current node
        - h(n) is the heuristic estimate of going from current node to final node
- This is the basic pseudocode:
```python
'''
    define class Node
        user
        f(n)

    frontier = []
    visited = []

    while True:
        if frontier is empty:
            return None
            break
        Get lowest f(n) user
        remove from frontier
        check if in explored set
        if explored:
            continue
        else:
            add to explored set
        f(n) >= threshold:
            return user
        get_neighbours and add to the frontier, if not in frontier
'''
```
- The perosnalized page rank algorithm loops over each person in the database and for each person it calculates their page rank using the personalized page rank formula (page rank = (1 - d) * personalized vector + d * Sum for all neighbours for value -> (page rank of neighbor / number of neigghbors)). We need to take into account whether someone can land on a user randomly, simulating bored random surfers (like in traditional Page Rank). The teleportation step always takes you back the start user in teh personalized page rank. 
We keep iterating the page rank algorithm until it has iterated a certain amount of times (defined by the max_iterations in the code) or when the total changes in the page ranks is below a threshold
- Basic pseudocode for Personalized Page Rank algorithm:
```python
'''
Create a graph of all users as nodes 
Assign each node a rank of 0
Assign the user node a rank of 1

page_rank

Loop for max iterations:

    new_rank = {}

    for user in page_rank
        get neighbors of current user
        
        if no neighbors:
            continue

        sum = 0
        for neighbor in neighbors of current user:
            sum += page rank of neighbour /  len (number of neighbours of this neighbor)

        page rank of current user += (1 - d) * personalized_vector + d * sum

    if sum of the total change < threshold:
        break
        
return page_rank
'''
```
### Bug: Personalized Page Rank didn't work as intended
- The formula I used was faulty
- What I did:
    - pr = (1 - d) * personalized_vector + d * sum ....
    - I assumed personalized vector would be the similarity/compatibility score
### Solution:
- The personalized vector is suppsoe to add to the page rankings if users randomly land on that user
- Hence if the node for which the page rank is being calculated is not the start user, then a value of (1-d) is not added to the page rank
- This correctly simulates if user teleports to the starting user

    I was manually teleporting using if statemtns
### Next steps
- Need to add the user values from the Personalized Page Rank algorithm in the `f(n)` function of the A* search to create the hybrid recommendation system
- Need to find a way to recommend user at specific time (Could possibly store the last time user was recommended a user and based on that recommend them a new user after every set time interval)
- Need to test and refine the recommendation system

## Date: July 29 - August 1
### Goal: Refine UI/UX
- My current UI and UX is quite poor as I focused more on functionality and features rather that user experience. Cluttered UI directly impacts user engagement and navigation efficiency. Redesigning for clarity improves usability
### What I learned
- Explored and integrated lightweight animation libraries:
    - AOS, for scroll based animations (such as fade-up)
    - Purecounter, for animated counters

    - Both are zero-dependency and easy to plug in
- DRY concept is to **Don't Repeat Yourself**, this is highly important for neat and scalable code. My previous profile page had duplicated logic, which made it hard to trace and debug. Therefore, it is vital to keep my code DRY
- Python, Javascript and CSS each have their own standard conventions for variable cases
    - Python (Django, Flask, etc.):
        - Variables/Functions: snake_case 
        - Classes: CamelCase
    - JavaScript (React, Node.js, etc.):
        - Variables/Functions: camelCase
        - Classes/Components: PascalCase
    - CSS Class Names/HTML Attributes: kebab-case
    - HTML/CSS:
        - Class Names/Data Attributes: kebab-case

    - I previously mixed styles without consistency, which hurt readability. Consistent casing is more important than I initially thought, especially in larger codebases.
### What I did
- Added edits to the home page (which is also visible to users who are not logged in)
- Created a intorduction section with statistics such as number of alumni , number of countries, and different carrers the alumni ave
- Just below the introduction section is 'take action' section, that has cards that take users to different parts of the website:
    - One for becoming a mentor
    - One for accessing mentor directory 
    - One for accessing alumni directory
- These cards are nice way for users to learn about the features provided on the website 
- I also edited models to have more intuitive names
#### Profile Page
- Completely changed the profile page view and profile edit functionality.
    - The previous profile page had becomed too clutered as there were now many fields and each field had a pencil icon next to it which made it incredibly unpleasing to look at and wasnt functional. T=The JavaScript logic relied on scattered event listeners and inconsistent element IDs, which introduced bugs and complexity
    - I switced to a more minimalistic look so that it is more intuitive for users
    - I also seperated fields into different sections and each section has its own edit button (instead of each field having its own edit button as in the previous approach)
        - Personal Information
        - Bio Section
        - Education
        - Skill
        - Goals
        - Career
    - The career section asks users whether they are employed or not through radio buttons
        - The buttons trigger JavaScript that sends an AJAX request to Django, updating the `has_job` field and dynamically toggling the visibility of the career section based on the response.
    - On validation errors (e.g., empty fields or invalid graduation year), an error message is rendered and its visibility is set to block
- For editing information, instead of using javascript, I directly send information to Django as it is much more scalable easier to organise
- Each section has its own URL route in `views.py`
#### View Profile
- When users now visit a users profile page, they have the option to both conenct and Request them as mentor if they are a mentor
- If any of the button is clicked a message is shown telling users how they'll be updated if they request is updated: 
`Once None accepts the request, you can chat with them here`
- A link which redirects to the chat is also provided
#### Messaging app
- Implemented a separate, interactive messaging section for the users
- The app is divided into two key areas:
    - Contact List: Displays the user's contacts and enables selection to start conversations
    - Messaging Space: Dynamically updates to display conversations based on the selected contact
- Dynamic Contact List:
    - Contacts are loaded asynchronously using JavaScript to fetch the list from the server
    - The contact list is rendered dynamically on the client side for a faster, more responsive UI
- Clicking on a contact in the list opens the corresponding conversation in the messaging space on the right side of the screen
- Each card is a link that loads the page with the corresponding messages.
- A search bar is integrated into the contact list, enabling users to filter and search for contacts by name dynamically.
- The search queries are handled client-side, improving performance and responsiveness.
### Bug 1: Validation error messages were not shown
- While implementing form validation for the user profile page, I attempted to display error messages by passing a query string when  redirected 
- However, eventhough invalid data was submitted, no error message appeared on the redirected page.
### Solution:
- The issue was with how I attempted to include the error message in the redirect() call in Django
- I was incorrectly assuming that keyword arguments in redirect() would be for the query parameters in the resulting URL
- Incorrect syntax:
    ```python
    redirect("profile", message = "Graduataion a valid number")
    ```
- Correct syntax:
    ```python 
    redirect("profile") + "?message=Graduation%20year%20must%20be%20a%20valid%20number"
    ```
### Bug 2: AJAX request was not working
- While implementing profile updates via AJAX, I encountered a persistent Uncaught TypeError in the browser console whenever a fetch request was made to update user data. The error indicated that the response object was being accessed incorrectly or prematurely.
### Solution:
- My `.then` was inside the fetch request. Since it is synchronous it didnt work
- The issue came from improper chaining of the .then() method
- I had nested .then() inside the fetch() call itself, which led to incorrect promise handling. 
- Specifically, I was attempting to handle the response synchronously, without awaiting the resolution of the initial fetch promise.
- Once the .then() chain was moved outside the fetch() call, the promise resolved as expected and the AJAX request executed without errors
### Bug 3: Messaging Page Returned 404 Error
- Accessing the messaging page at /messaging/messages/ consistently returned a 404 Not Found error
### Solution:
- I was attempting to visit the URL path /messaging/messages/, but I had not actually defined this path in urls.py
```python
path("messages", views.messages, name="messages")
```
- This only works for /messaging/messages, not /messaging/messages/ (with a trailing slash)
- I implemented the correct url and I also double-checked the URL patterns in urls.py and used Django's {% url %} template tag where appropriate to avoid hardcoding paths incorrectly.
- Lesson learnt:
    - The Network tab in browser DevTools is incredibly helpful for debugging broken links or unexpected 404s by showing exactly what request is being made
### Next steps:
- Add another section on the messageing app where users can see any requests, hwen users request to connect.
- One section can toggle between showing teh connection requests and showing messages

## Date: August 3
### What I did
- Created a seperate alumni directory where users can search for alumni by their name and filter them batch year and university. 
- Clicking on a profile:
    - In the Mentor Directory: shows a Request Mentor button.
    - In the Alumni Directory: shows a Connect button to send connection requests.
- Revamped the Mentor Dashboard:
    - I redesigned the mentor dashboard to better support request managment
    - I add kety metrics at the top that show the total requests made, accepted requests and pending requests
    - I added an interactive table with tabbed views:
        - All, Accepted and Declined requests
    - Each row contains the date when the request was made, shows the current status and allows actions.
    - When `Accept` is clicked from the actions, it marks the `accepted` value as True in teh backend and also runs the `create_chat_room` function from `messaging.utils` which now creates a Group model for the two users. This group can now be accessed in both the mentor and mentees Messaging app.
- I made the chat app responsive for mobile use too. I added an additional value to the context, `current_chat`, which informs whether the message section should be open or not. I used this with Jinja to conditionally not show the sidebar on smaller screens. This makes it so that users don't need to scroll down to view the messages when they are using the website on mobile. I additionally also added a back button on the
- I also grouped similar pages together in the navigation bar to reduce clutter by using dropdowns
    - Dashboard: contains Home page, Profile, and the Activity Hub(messaging app)
    - Mentorship: contains Mentor directory and Mentor dashboard/mentor sign up
    - Explore: contains both the alumni and mentor directory
### Bug 1: Messages were not being loaded
- When I clicked on a newly added contact in the message app, the message section on the right would show the default "Select a conversation message", eventhough the WebSocket Handshake was intitiated and the connection was made
- Clicking on older contacts loaded the correct messages
### Solution:
- I had previously made a condition to only load the chat section if the Backend successfully retrived the messages and user details
- However, this meant that for new contacts, who didnt have any messages, the app was not loading the message section as it didn't meet the condition
- I removed the condition
### Bug 2: Message app was not working on mobile screens
- I initially used Javascript to toggle between the visibility of teh `.chat-wrapper` and the `.sidebar-wrapper` based on screen width and when a contact was clicked
- However, clicking a contact perfomed a full page reload, so the chat section flashed in but went back to the side bar
### Solution:
- Instead of toggling the two views with Javscript, I used Django to determine which sections should be visible.
- I added a `current_chat` field which was passed to both `message.html` and `messages.html` and helped them determine what to show.
### Next Steps:
- I now need to refine and finish my AI and find how exaclty I am going to suggest users other contacts (for example is it going to be on a weekly bases or am I going to store information about the last time the user was recommended someone and accordingly recommend them)
- I also need to create a way users can accept or decline requests for Connection. I am thinking of maybe integrating this feature on the "Acitivity Hub"

## Date: August 4
### What I did
- Implemented a sidebar on the profile page displaying all pending connection requests for the user.
- Each request is presented as a card with three action buttons:
    - View: to view the profile 
    - Accept & Decline: triggers an AJAX request to update the connection status in the database. Once done, the corresponding card is dynamically removed from the UI
- Refined the A* modified search heurisitic to include the personalized page rank algorithm
    - ```python
        def h_n(profile1, profile2, normalized_page_ranks, alpha=ALPHA, beta=BETA):
        similarity_score = calculate_score(profile1, profile2)
        ppr_value = normalized_page_ranks[profile2]

        heuristic = ALPHA * (1-similarity_score) + BETA * (1-ppr_value)
        ```
    - This new heuristic takes into account both the similarity score and the personalized page rank. `ALPHA` and `BETA` are used to determine which rank/score should be valued more
    - Currently, I've set both values to 0.5 so local similarity and global connectivity are both valued the same
- Added a modal on the directory page that shows the recommended user and the compatibility score. The directory view calls the `recommend` function.
### Bug: AI module was constantly raising key errors
- When the code tried to access a user in the neighbors dictionary, a key error was raised
### Solution:
- All three of the files (`personalized_page_rank.py`, `a_star_search.py`, and `utils.py`) had conflicting use of `Profile` and `Users` instance
- Therefore, I ensured that all of the functions use the `Profile` instance. Only the `recommend` function in `recommender.py` takes a `Users` instance which it then uses its `Profile` instance and passes it on to the other functions.
### Reflection
- Initially, I rendered teh AI recommendation modal directly in the Django view during the directory page load. However, this meant that every time a user visited the page, the recommendation engine was triggered too, causing a noticable delay, especially when I tried by adding many users in the database. It took noticeable time even with just 12 Users
- I tried to optimize the code by storing the results of `get_neigbors` function in a variable instead of calling it everytime in the loop. This did reduce the number of queries made to the database, but the delay was still noticeable
- I then switched to a different approach. I loaded the directory first and used Javascript to send an AJAX request so that the users dont notice the delay as the directory is loaded and once the recommendation engine outputs a result, it is displayed on the modal.
- This approach does seem to work for the time being but will only work if users stay on the directory long enough. If they click on a profile, it may cancel the request
- I then switched to a different approach: instead of blocking the page load, I rendered the directory first and used JavaScript to send an AJAX request in the background. This way the directory loads instantly and the recommendation modal appears only once the AI engine finishes processing, making the experience feel seamless
- While it does improve the responsiveness, it has a tradeoff: it only works if the ysers stay on the page long enough. If they, for example click a profile, the modal may not appear
- I am considering moving the modal and related Javascript to the base template. This way, recommendations can be triggered regardless of which page the user is on
