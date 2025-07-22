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
- **Decision** Chose to prefill form with user data available for better UX as users won't need to enter same information again.
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
- **Decision** Needed to decide whether to keep using a single app for the project or seperate out into multiple apps. 
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
- **Decision** I initially wrote the code using a synchronous approach, but later switched to an asynchronous implementation as it proved to be significantly more efficient and better suited for handling multiple users concurrently
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
