This is a robust, data-driven backend designed to power a modern blog platform. It features a complete RESTful architecture with automated metadata calculation and a personalized user engagement system.

🎨 For Designers & Frontend Devs
This API is built to support high-fidelity Figma designs. Key integration points:

Dynamic Icons: The backend provides separate states for Likes (Public), Stars (Personal), and Bookmarks (Read Later).

Automated UI Elements: The API automatically calculates "Reading Time" and "Relative Timestamps," reducing the logic needed on the frontend.

🛠️ Backend Features
Automated Read-Time Calculation: An algorithm that computes reading time based on word count.

Public Engagement: Trackable like_count visible to all users.

Personalized User Collections: Individual "Star" (Favorites) and "Bookmark" (Read Later) lists unique to each logged-in user.

Auto-Ordering: Global configuration to ensure the GET list always returns the newest posts first.

Relational Data Mapping: Automatic mapping of blog posts to specific user profiles (Authors).
