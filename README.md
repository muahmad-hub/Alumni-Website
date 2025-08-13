# Alumni Website - AI-Powered Networking Platform
## Table of Contents
- [Quick Overview](#quick-overview)
- [Demo](#demo-and-screenshots)
- [Architecture](#architecture)
- [Key Features](#key-features)
- [Technical Details](#technical-highlights)
- [Motivation](#motivation)
- [Links](#links)
## Quick Overview
- **Purpose:** Intelligent alumni networking & mentorhsip platform that keeps graduates and current students connected and supports growth.
- **Built by:** Solo project after completing CS50X, CS50 Web, and CS50 AI. Started after feeling that students can benefit grately from mentorship and connections with peers
- **Key Tech:** Django, PostgreSQL, WebSockets, BERT + SVM, custom A* + Personalized PageRank recommendation engine.
- **Highlights:**
    - Recommendation system that uses custom A* + Personalized PageRank algorithm to recommend most compatible alumni to users.
    - AI skill & goal categorization with 72-80% accuracy, used by recommendation system
    - Real-time chat with Django channels and WebSocket
    - Fully integrated full-stack system (frontend, backend, database, ML, networking).
>For more details: [Technical Details](docs/technical_details.md) and [Dev logs](docs/dev_logs.md)
## Demo and Screenshots
## Architecture:
- **Frontend:** HTML, CSS, JavaScript.
- **Backend:** Django (Python). 
- **Database:** PostgreSQL.
- **AI/ML:** BERT embeddings + SVM classifiers used to create a supervised learning model built on my own database; A* + Personalized PageRank recommendation engine.
- **Messaging:** Django Channels with WebSockets & in-memory layer.
## Key Features
- **User profiles:** Searchable alumni and mentor database with editable user info
- **Mentorship program:** Request, accept, & allow mentors to manage requests seamlessly through their personalized dashboard
- **Dynamic Directory Search:** Name/skill + filters by university & batch year
- **Real-time chat:** WebScoket-powered messaging
- **AI Categorization:** BERT + SVM model to classify skills and goals
- **Recommendation Engine:** A*-like heuristics + Personalized PageRank
## Technical Highlights
>See [Technical details](docs/technical_details.md)
- Recommendation Engine:
    - Models users as nodes in a weighted graph.
    - A* heuristic prioritizes skill, goal, education, and location compatibility.
    - Personalized PageRank surfaces globally relevant but non-obvious matches.
    - Optimizations: caching, vectorization, pruning, and batch processing.
- AI Classifier:
    - Supervised ML with BERT embeddings + SVM.
    - Goal classifier: 81% F1 score; Skill classifier: 72% F1 score (500-sample dataset).
    - Integrated into user profile updates.
- Messaging System:
    - Full-duplex WebSocket channels for low-latency communication.
    - Saves messages to PostgreSQL; broadcasts via memory channel layer.
## Motivation
As a relatively new student, I found it difficult to navigate sixth form, prepare for university applications, search for internships and volunteering opportunities, and discover meaningful activities. I often wished I could connect with seniors who were already at university — people who had been through the same process and could offer guidance.

This project was built to make that possible: to give current students an easy way to find and connect with alumni who can provide mentorship, share advice, and open doors to opportunities.

This platform also helps graduates and peers maintain meaningful connections after school, so that friendships and professional networks could continue to grow over time.
## Links
- My Dev Log and Learning Journal: [dev_logs.md](docs/dev_logs.md)
- Technical details: [technical_details.md](docs/technical_details.md)