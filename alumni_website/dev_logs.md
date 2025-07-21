# Dev Logs

## Date: July 1
### Moved Flask-based project to Django-based
- Added Django-based authentication system, profiles and linked project to PostgreSQL on local host
- Created a profile edit feature
- Currently using a single app for all features

## Date: July 2
### Feature: Alumni Directory, Clickable cards in directory, and added sepereate profile edit page
- Users could already edit profile once they sign up, but for additional editing I created a seperate edit page.
- Directory allows users to search based on their name

## Date: July 3
### Feature: Created Mentor system
- Added link in navigation to allow users to sign up through form
**Decision** Chose to prefllform with user data available fro better UX
-Dashboard is availabel to suers who signed up to become mentors
-Dashboard allows users to see all their mentor requests
- Edited directory to allow users to search by skills

## Date: July 4
### Aded advanced filtering
- Directory allows users to search by batch year and University for better searching Mentors
**Problem** Univeristy and Batch year search would overide each other due to ineffecient conditions used for querying 
**Solution** Used Q object in Django for complex querying and added all the queries into a seperate variable and queried database only at the end. The previous approach would qury the database in each if statment which lead to incorrect filtering of alumni in teh directory

## Date: July 5
**Decision** Needed to decide whther to stick with a single app project or seperate out into multiple apps. I decided to use seperate apps as it would allow the code to be more organised and the project to be scalabale
- Seperated the project into 5 apps: 
    core
    authentication
    profiles
    directory
    mentorship
- Added a single template and static folder

## Date: July 20
### Feature: Added a very basic prototype of a chat feature
- This day was more about learning how to actually implement a chat feature and what technolgoies to use
- Plan on using Websockets and Redis along with HTMX for dynamic requests

## Date: July 21
### What I learnt
- Learn about requests and server, HTTP is a request-response model. The client has to initialize the communication by sending a request to the server. If the request is valid then the server will reply back with a response. This model is inneffecient for real-time chat because data is continuously being transffered from multiple users to the server and from the server. This would require polling where the client would have to request the server after every set time. 
- Using WebSocket protocol is much more effecient for this purpose as it is a protocol that supports bidirectional data transfer. It starts off by a handshake proccess where the client requests the sever and if valid the server responds back. After this initial step the WebSocket connection is made and data can be sent from and to the server with ease.
- Channels are like mailbox for each user. When a WebSocket connection is intitiated by a user, a channel specific to that user is also created. Channels help the server route data towards the users. Without it the server wont know where to route and hence send messages. 
- The proccess of sending data can be synchronous (works like a queue, waits for one line of code to be completed and then runs the next) or asynchronous (multipel lines of codes can be run while it waits for some previous code to finish its work). Both can be used for sending messages. However, asynchronous code will be much more effeicient for sending data for real time chats.
### Decision
- I intitially created the code to be synchronous, but later withced to being asynchronous as it was much more effeicient and better for many users
### TALK ABOU TTHE BUG