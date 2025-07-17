# Alumni Mentor Match

## Quick Description
**Alumni Mentor Match** is a full-stack application whose main purpose is to allow Alumni's to connect with mentors and mentees and receive guidance. This is a professional matching and guidance platform, enabling alumni to search, request, accept, and manage mentoring relationships with a structure built around mentorship rather than social interaction.

### Key Features:
- Secure user authentication (login/signup).
- Profile creation and editing.
- Mentor discovery with skill-based search.
- Request workflows for mentor-mentee connections.
- Role-based dashboards for mentors and mentees.
- Live feedback through request statuses (Pending/Accepted/Declined).

## Inspiration
Having recently changed schools, I learned the importance of mentorship and guidance from others, especially from experienced alumni. Throughout my academic journey, I often found that having advice from someone who had been through similar experiences could have been incredibly valuable. This inspired me to build **Alumni Mentor Match**, a platform where alumni can register either as mentors or mentees and offer or receive professional guidance. 

The lessons I learned in CS50 Web helped me implement a prototype of this project, leveraging both Django for backend functionality and JavaScript for a dynamic frontend experience.

## Technology Stack
- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript
- **Database**: PostgreSQL (for scalability and relational data management)
- **Authentication**: Django's built-in user authentication system
- **Dynamic UI**: JavaScript for dynamic content updates and interaction with the backend



### Distinctiveness and Complexity
Alumni Mentor Match is fundamentally different from any of the CS50 Web course projects, especially Project 4 (Social Network), in both purpose and technical structure.

### Purpose-Driven vs. Open-Ended Interaction
Unlike Project 4, which simulates a general-purpose social network with followers, posts, and likes, this application is a mentorship platform. The goal is not to create social connections or interactions but rather to facilitate guided mentorship between alumni and students based on skills, availability, and domain expertise. There are no user-to-user feeds, likes, comments, or followers. Instead, there's a request-based mentor matching system, focused on enabling mentorship relationships.

### Structural Differences
Project 4 centers around a post/feed system with timelines and comment threads. My project revolves around role-based flows: mentor vs. mentee. The entire experience and permissions change depending on whether you're a mentor or not.

It uses real-time, skill-based mentor searching, rather than profile browsing or friends lists.

The request system is workflow-based, involving dynamic status updates, and custom dashboards showing current mentoring relationships or pending requests.

### Technical Complexity
This application introduces many-to-many relationships, custom model design, and user experience logic that goes beyond any single feature in the course. Some examples:

A MentorMatch model that connects two users via a formalized request and approval workflow.

### Dynamic front-end behavior using JavaScript, including:

Real-time filtering of mentors

Inline feedback updates

Conditional UI rendering (e.g., buttons and icons changing depending on database status)

The database schema includes separate models for skills and languages, avoiding repetition and allowing scalable search/filter logic.

There's also thoughtful access control and form prepopulation, enhancing UX in meaningful ways.

### Role-Based UI and Logic
Depending on whether the user is a mentor or not:

They are shown different dashboards.

Their form options and access are restricted or enhanced.

Their ability to view or interact with mentoring data is controlled.

This is more than a feed app — it's a real-world, purpose-built web platform with structured user flows, which makes it both distinctive and technically more demanding than the provided course projects.

**********************************************************
## How It Works

### Authentication:
- **Login/Signup**: Users can sign up with just an email and password. For a smooth UX, I kept the sign up simple with minimal fields.
- **Profile Creation**: After signing in, users are prompted to create a professional profile when they click Profile on the top navigation bar.

### Features:
- **Profile**: Users can view and edit their profiles, which include career details, education, skills. Profiles can be edited directly on the page or via a dedicated edit page.
- **Become a Mentor**: Users can apply to become a mentor by filling out a form with relevant details such as availability, skills, and languages. Once submitted, they are redirected to their Mentor Dashboard.
- **Mentor Search**: The Mentor Directory allows users to search for mentors based on specific skills. A dynamic search bar is used for real-time filtering.

### Dynamic Interaction:
- **Mentor Directory**: Mentor cards are dynamically generated using JavaScript and fetched from the Django backend. When a mentor is found, their skills are displayed, and the user can send a mentor request.
- **Request Workflow**: Mentor requests are tracked with statuses of "Pending", "Accepted", or "Declined". Mentors can manage these requests from their dashboard. The dashboard allows users to see the pending requests and the accepted requests.
- **Home Page for Mentees**: Mentees are able to see their pending requests on the home page along with basic information like Name, and skills of the mentor who they requested


## Database Design

To ensure data is normalized and easy to manage, I used the following models:

1. **User Model**:
   - Stores only essential authentication data (email and password).

2. **Profile Model**:
   - Linked to the `User` model with a one-to-one relationship.
   - Stores project-related details like career, location, education, and bio.
   - I kept `User` and `Profile` model seperate for better scalability and organisation.
   
3. **Mentor Model**:
   - Stores mentor-specific information such as availability and industry.
   - Populated when users choose to become mentors through filling a form on the webstie.

4. **Skills and Languages Models**:
   - These models are separated from the Mentor model to avoid redundant data.
   - Each mentor can have multiple skills and languages as they have a many-to-many relationship.

5. **MentorMatch Model**:
   - Tracks requests from mentees to mentors. The `accept` field indicates whether the mentor has accepted or declined a request.
   - If the accept field is None, it means that the mentor has still now acknowledged the request.


## UX/UI Design Decisions

### Profile Page:
- **Dynamic Editing**: I had to make a UX decisison about how users shoudl be allowed to edit their Profile information. Therefore, I went for a hybrid decision. - If the user has never added profile info, a pencil icon appears next to fields. After submission, the icon disappears to reduce clutter and show completed profile status.
- **Hybrid Editing**: Users can also access a dedicated "Edit Profile" page for a more traditional form-based approach when they have edited their information and want to edit it later on.

### Mentor Directory:
- **Real-Time Search**: The search bar at the top of the Mentor Directory dynamically filters mentors based on skills. This is done through JavaScript sending requests to Django to fetch relevant data.
- **Mentor Cards**: Mentors are displayed in cards with relevant details like their name, skills, and industry. If no mentors are found, the system displays a "No mentors available" message.

### Navigation & Access Control
- Unauthenticated users only see "Login" and "Signup" options and cannot access main pages.
- Once logged in, the navigation updates to include: Profile, Mentors, Become a Mentor, and Logout.

### Form Design
- I used a datalist tag along with option tag for the skills field. The template uses data sent by Django and loops over it to show suggested skills that other users have added. 
- The form also automatically fills in some of the information in the form such as name, email and industry/field.