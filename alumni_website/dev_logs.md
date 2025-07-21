# Dev Logs

## Date: July 1
### Migration from Flask to Django & Initial Setup
- **What I did:** Migrated the project from Flask to Django to leverage Django's built-in features and scalability. Set up Django authentication, user profiles, and connected the project to a local PostgreSQL database.
- **What I learned:** Understood the differences between Flask and Django, especially in terms of project structure and built-in user management. Learned how to configure Django settings for PostgreSQL and how to use Django's ORM for database operations.
- **Reflection:** The migration was challenging but rewarding. Django's admin and authentication system saved a lot of time compared to building from scratch in Flask.

## Date: July 2
### Alumni Directory & Enhanced Profile Editing
- **What I did:** Implemented the Alumni Directory feature, allowing users to search for alumni by name. Added clickable cards for each alumnus. Created a separate profile edit page for more flexible user experience.
- **What I learned:** Practiced using Django views and templates to display dynamic content. Learned how to pass data from the backend to the frontend and handle user input for searching. Improved my understanding of Django's template language and form handling.
- **Reflection:** Building the directory helped me see the power of Django's querysets and how to efficiently filter and display data. Creating a dedicated edit page improved the UX and made the app feel more professional.

## Date: July 3
### Mentor System & Dashboard
- **What I did:** Added a mentor signup form and dashboard. Users can now sign up as mentors, and mentors have a dashboard to view and manage their mentorship requests. Enhanced the directory to allow searching by skills.
- **What I learned:** Learned how to design many-to-many relationships in Django and how to prefill forms with user data for better UX. Practiced using Django's decorators for access control and dashboard logic. Improved my skills in designing user flows and conditional rendering in templates.
- **Reflection:** The mentor dashboard required careful planning of user roles and permissions. Prefilling forms made the signup process smoother and more user-friendly.

## Date: July 4
### Advanced Filtering & Query Optimization
- **What I did:** Added advanced filtering to the directory, allowing users to search by batch year and university. Refactored the query logic to use Django's Q objects for complex filtering.
- **What I learned:** Discovered the importance of query optimization. Initially, each filter condition queried the database separately, leading to incorrect results and inefficiency. By combining conditions with Q objects and querying only once, I improved both accuracy and performance.
- **Reflection:** This was a key learning moment about how database queries work in Django and why efficient querying is crucial for scalability. I also learned to debug and test complex filter logic.

## Date: July 5
### Project Structure & Modularization
- **What I did:** Decided to split the project into multiple Django apps (core, authentication, profiles, directory, mentorship) for better organization and scalability. Centralized static and template files.
- **What I learned:** Understood the benefits of modularizing a Django project. Each app now has a clear responsibility, making the codebase easier to maintain and extend. Learned how to configure Django to use shared static and template directories.
- **Reflection:** This decision made the project much more manageable. I now appreciate the Django philosophy of "apps as building blocks."

## Date: July 21
### Chat Feature Prototype & Real-Time Technologies
- **What I did:** Started building a basic chat feature as a prototype. Researched and experimented with Websockets, Redis, and HTMX for real-time updates and dynamic requests.
- **What I learned:** Gained a foundational understanding of real-time web technologies and how they integrate with Django. Learned about the challenges of implementing live chat, such as message broadcasting and state management. Explored how HTMX can simplify dynamic UI updates without full page reloads.
- **Reflection:** This was a big step outside my comfort zone. Even though the chat is still basic, I now have a roadmap for making it fully real-time. The research into Websockets and Redis will be valuable for future features.

