# BLOGGING SITE: SIMPLY SAID
## Comprehensive Technical Documentation

**Project Date:** January 2026  
**Repository:** `Krish-DevCom/BLOGGING-SITE-SIMPLY-SAID`  
**Primary Language:** Python (Django) + React  
**Status:** Active Development

---

## TABLE OF CONTENTS

1. [Project Overview](#project-overview)
2. [Tech Stack](#tech-stack)
3. [Database Design & Models](#database-design--models)
4. [Backend Architecture](#backend-architecture)
5. [API Endpoints](#api-endpoints)
6. [Authentication System](#authentication-system)
7. [Features & Functionality](#features--functionality)
8. [Frontend Structure](#frontend-structure)
9. [Configuration & Setup](#configuration--setup)
10. [Interview Talking Points](#interview-talking-points)

---

## 1. PROJECT OVERVIEW

### Purpose
A full-stack blogging platform where users can:
- Create, read, and manage blog posts
- Discover blogs through search and category filtering
- Interact with content via likes, stars (favorites), and bookmarks
- Manage personal collections (favorites list)
- Browse trending and categorized content

### Key Features
- **User Authentication:** Token-based authentication
- **Blog Management:** CRUD operations with full metadata
- **Social Interactions:** Like, star, and bookmark functionality
- **Smart Filtering:** Search by keywords, category-based discovery
- **Read Time Estimation:** Auto-calculated based on word count
- **Image Support:** Cover image uploads with media serving

---

## 2. TECH STACK

### Backend
```
Framework:     Django 5.2.10
REST API:      Django REST Framework 3.16.1
Authentication: Django REST Framework Token Auth
CORS:          django-cors-headers 4.9.0
Image Processing: Pillow 12.1.0
Database:      SQLite3 (Default) - Scalable to PostgreSQL
```

### Frontend
```
Framework:     React 18+ (with Vite)
Build Tool:    Vite
Features:      HMR (Hot Module Replacement), ESLint enabled
```

### Full Requirements
```
asgiref==3.11.0
Django==5.2.10
django-cors-headers==4.9.0
djangorestframework==3.16.1
pillow==12.1.0
sqlparse==0.5.5
```

---

## 3. DATABASE DESIGN & MODELS

### 3.1 Blog Model (Core)
**File:** `backend/posts/models.py`

**Fields:**
- `title` → CharField(max_length=200)
- `content` → TextField() [Supports Markdown/HTML]
- `cover_image` → ImageField(upload_to='blogs/')
- `user` → ForeignKey(User) [Blog Author]
- `created_at` → DateTimeField(auto_now_add=True)
- `updated_at` → DateTimeField(auto_now=True)
- `likes` → ManyToManyField(User, related_name="liked_blogs")
- `stars` → ManyToManyField(User, related_name="starred_blogs")
- `bookmarks` → ManyToManyField(User, related_name="bookmarked_blogs")
- `category` → CharField(choices=CATEGORY_CHOICES)
- `tags` → ManyToManyField(Tag)
- `read_time` → @property (auto-calculated)

**Category Options (EXACT STRINGS FOR API):**
- Culture
- Travel
- Food
- Business
- Tech
- Life

**Read Time Calculation:**
```
Formula: word_count / 50 (approximates 200 wpm reading speed)
Returns: minimum 1 minute
```

**Key Design Decisions:**
- ManyToMany for interactions allows efficient querying of user's liked/bookmarked blogs
- Auto-timestamps for sorting and filtering
- Read time auto-calculated, not stored

---

### 3.2 Tag Model
**File:** `backend/posts/models.py`

**Fields:**
- `name` → CharField(max_length=50, unique=True)

**Usage:**
- Tags are dynamic and created on-demand
- Frontend sends tags as list of strings: `["tech", "coding", "python"]`
- Backend auto-creates tags if they don't exist
- Enables content discovery and filtering

---

### 3.3 User Model
**Extends:** `django.contrib.auth.models.User`

**Fields Used:**
- `username` → Unique identifier
- `password` → Hashed password
- `liked_blogs` → Reverse relation (from Blog model)
- `starred_blogs` → Reverse relation (from Blog model)
- `bookmarked_blogs` → Reverse relation (from Blog model)

---

### 3.4 Favourites Model
**File:** `backend/auth_app/models.py`

**Fields:**
- `user` → ForeignKey(User, on_delete=models.CASCADE)
- `blog` → ForeignKey(Blog, on_delete=models.CASCADE)
- `created_at` → DateTimeField(auto_now_add=True)

**Meta:**
- `unique_together = ('user', 'blog')` [Prevent duplicates]
- `ordering = ['-created_at']`

**Purpose:**
- Separate collection system from likes
- Allows users to explicitly save blogs to favorites list
- Different from "likes" (more like bookmarks in other platforms)

---

## 4. BACKEND ARCHITECTURE

### 4.1 Project Structure
```
backend/
├── backend/                 # Main project config
│   ├── settings.py         # Django configuration
│   ├── urls.py             # URL routing (main)
│   ├── wsgi.py
│   └── asgi.py
│
├── posts/                  # Blog app
│   ├── models.py           # Blog, Tag models
│   ├── views.py            # Blog views (list, detail, interactions)
│   ├── urls.py             # Blog routes
│   ├── serializers.py      # Data serialization
│   └── migrations/
│
├── auth_app/               # Authentication app
│   ├── models.py           # Favourites model
│   ├── views.py            # Login, Signup, Collections
│   ├── urls.py             # Auth routes
│   ├── serializers.py      # User, Favourites serialization
│   └── migrations/
│
├── media/                  # User-uploaded images
├── db.sqlite3              # Database file
└── requirements.txt        # Dependencies
```

### 4.2 Settings Configuration
**Key Settings:**

```python
# Security
DEBUG = True                          # Set to False in production
SECRET_KEY = 'django-insecure-...'  # Use environment variables
ALLOWED_HOSTS = []                  # Configure for production

# Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',              # DRF
    'corsheaders',                 # CORS support
    'posts',                       # Blog app
    'auth_app',                    # Auth app
    'rest_framework.authtoken',    # Token authentication
]

# CORS Configuration
CORS_ALLOW_ALL_ORIGINS = True      # Allow all origins (dev only)

# Media Files
MEDIA_URL = '/media/'              # Public URL for images
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

---

## 5. API ENDPOINTS

### 5.1 Blog Endpoints (`/api/blogs/`)

#### 1. Get All Blogs (with filtering)
```
GET /api/blogs/
```

**Query Parameters:**
- `search=<string>` - Search in: title, content, category, tags
- `category=<string>` - Filter by category (exact match)

**Examples:**
```
GET /api/blogs/                           # Get all blogs
GET /api/blogs/?search=python             # Search for "python"
GET /api/blogs/?category=Tech             # Get only Tech category
GET /api/blogs/?search=react&category=Tech  # Combine filters
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Getting Started with Django",
    "content": "Django is a powerful...",
    "cover_image": "https://example.com/media/blogs/cover.jpg",
    "author_username": "john_doe",
    "created_at": "Jan 15, 2026",
    "updated_at": "2026-01-15T10:30:00Z",
    "read_time": 5,
    "like_count": 12,
    "category": "Tech",
    "tags": ["django", "python", "web-development"]
  }
]
```

---

#### 2. Create a New Blog
```
POST /api/blogs/
Content-Type: application/json
Authorization: Token <auth_token>
```

**Request Body:**
```json
{
  "title": "My First Blog Post",
  "content": "This is the main content...",
  "category": "Tech",
  "tags": ["coding", "tutorial"],
  "cover_image": "<file>"
}
```

**Response (201 Created):**
```json
{
  "id": 5,
  "title": "My First Blog Post",
  "author_username": "my_username",
  "created_at": "Jan 16, 2026",
  "category": "Tech",
  "tags": ["coding", "tutorial"],
  "read_time": 3,
  "like_count": 0
}
```

**Errors:**
- `400 Bad Request` - Invalid data
- `401 Unauthorized` - User not authenticated

**Valid Categories:**
Culture, Travel, Food, Business, Tech, Life

---

#### 3. Get Blog Details
```
GET /api/blogs/{id}/
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Getting Started with Django",
  "content": "Full markdown or HTML content...",
  "cover_image": "https://example.com/media/blogs/cover.jpg",
  "author_username": "john_doe",
  "created_at": "Jan 15, 2026",
  "read_time": 5,
  "like_count": 12,
  "category": "Tech",
  "tags": ["django", "python"]
}
```

**Errors:**
- `404 Not Found` - Blog doesn't exist

---

### 5.2 Blog Interaction Endpoints

#### 4. Toggle Like
```
POST /api/blogs/{id}/like/
Authorization: Token <auth_token>
```

**Response (200 OK):**
```json
{
  "status": "liked",
  "like_count": 13
}
```

**Toggle Behavior:**
- 1st POST → "liked", like_count: 13
- 2nd POST → "unliked", like_count: 12
- 3rd POST → "liked", like_count: 13

---

#### 5. Toggle Star (Favorite)
```
POST /api/blogs/{id}/star/
Authorization: Token <auth_token>
```

**Response (200 OK):**
```json
{
  "status": "starred"
}
```

---

#### 6. Toggle Bookmark (Reading List)
```
POST /api/blogs/{id}/bookmark/
Authorization: Token <auth_token>
```

**Response (200 OK):**
```json
{
  "status": "bookmarked"
}
```

---

### 5.3 Authentication Endpoints

#### 7. Sign Up
```
POST /signup/
Content-Type: application/json
```

**Request:**
```json
{
  "username": "john_doe",
  "password": "securepassword123"
}
```

**Response (201 Created):**
```json
{
  "id": 5,
  "username": "john_doe"
}
```

**Errors:**
- `400 Bad Request` - Username already exists

---

#### 8. Login
```
POST /login/
Content-Type: application/json
```

**Request:**
```json
{
  "username": "john_doe",
  "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "username": "john_doe",
  "message": "Login Successful"
}
```

**Error Responses:**
```json
// Wrong password
{ "error": "Incorrect Password" }  // 400 Bad Request

// User not found
{ "error": "User not found" }      // 401 Unauthorized
```

---

### 5.4 User Collections Endpoints

#### 9. Get User's Liked Blogs
```
GET /likedblogs/
Authorization: Token <auth_token>
```

**Response (200 OK):**
```json
{
  "user": "john_doe",
  "liked_blogs": [
    {
      "id": 1,
      "title": "Getting Started with Django",
      "like_count": 12
    }
  ]
}
```

---

#### 10. Get User's Bookmarked Blogs
```
GET /bookmarkedblogs/
Authorization: Token <auth_token>
```

**Response (200 OK):**
```json
{
  "user": "john_doe",
  "bookmarked_blogs": [...]
}
```

---

#### 11. Toggle Favourite
```
POST /favourite/{blog_id}/
Authorization: Token <auth_token>
```

**Response (200 OK - Added):**
```json
{
  "message": "Added to Favourites",
  "is_favourite": true
}
```

**Response (200 OK - Removed):**
```json
{
  "message": "Removed from Favourites",
  "is_favourite": false
}
```

---

#### 12. Get User's Favourite Blogs
```
GET /favblogs/
Authorization: Token <auth_token>
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "blog": {
      "id": 1,
      "title": "Getting Started with Django"
    },
    "created_at": "2026-01-15T10:30:00Z"
  }
]
```

---

## 6. AUTHENTICATION SYSTEM

### 6.1 Token-Based Authentication
```
Framework: Django REST Framework Token Authentication
Model: rest_framework.authtoken.models.Token

Flow:
1. User signs up → User account created
2. User logs in → Token generated and returned
3. Client stores token in localStorage
4. For protected endpoints → Include: Authorization: Token <token>
```

### 6.2 Protected Endpoints
These require `Authorization: Token <auth_token>` header:

```
POST /api/blogs/                    # Create blog
POST /api/blogs/{id}/like/
POST /api/blogs/{id}/star/
POST /api/blogs/{id}/bookmark/
GET /likedblogs/
GET /bookmarkedblogs/
POST /favourite/{blog_id}/
GET /favblogs/
```

### 6.3 Public Endpoints (No auth required)
```
GET /api/blogs/
GET /api/blogs/{id}/
POST /signup/
POST /login/
```

---

## 7. FEATURES & FUNCTIONALITY

### 7.1 Blog Management

| Feature | Implementation | Backend Support |
|---------|-----------------|-----------------|
| Create Blog | POST /api/blogs/ | ✅ Title, Content, Category, Tags, Cover Image |
| Read Blogs | GET /api/blogs/ | ✅ Full blog data with metadata |
| List All | GET /api/blogs/ | ✅ Sortable by date |
| Search | GET /api/blogs/?search=X | ✅ Searches 4 fields |
| Filter by Category | GET /api/blogs/?category=X | ✅ 6 categories available |
| View Details | GET /api/blogs/{id}/ | ✅ Complete blog content |

---

### 7.2 User Interactions

| Feature | Endpoint | Behavior | Count Display |
|---------|----------|----------|----------------|
| Like | POST /api/blogs/{id}/like/ | Toggle on/off | Returns `like_count` |
| Star | POST /api/blogs/{id}/star/ | Toggle on/off | Not counted |
| Bookmark | POST /api/blogs/{id}/bookmark/ | Toggle on/off | Not counted |

---

### 7.3 Collections & Curation

| Feature | Endpoint | Storage |
|---------|----------|---------|
| Liked Blogs | GET /likedblogs/ | ManyToMany relation |
| Bookmarks | GET /bookmarkedblogs/ | ManyToMany relation |
| Favourites | POST/GET /favourite/ & /favblogs/ | Separate model |

---

### 7.4 Smart Features

| Feature | Auto-Calculated | Usage |
|---------|-----------------|-------|
| Read Time | Yes (word_count / 50) | Displayed on cards |
| Timestamps | Yes (auto_now_add/auto_now) | Sort and filter |
| Tag System | Dynamic creation | Content discovery |
| Media Serving | Configured | Images uploaded to /media/ |

---

## 8. FRONTEND STRUCTURE

### 8.1 Tech Stack
- **Framework:** React 18+ (with Vite)
- **Build Tool:** Vite with HMR
- **Features:** ESLint enabled, React Router (implied)

### 8.2 Expected Pages/Components

```
Pages:
├── Home / Feed
│   ├── Blog List (with search & category filters)
│   ├── Blog Card (title, author, tags, read time, likes)
│   └── Category Sidebar (Culture, Travel, Food, etc.)
│
├── Blog Detail Page
│   ├── Full blog content
│   ├── Author info
│   ├── Interaction buttons (Like, Star, Bookmark)
│   └── Read time indicator
│
├── Authentication
│   ├── Sign Up Form
│   └── Login Form
│
├── User Dashboard
│   ├── My Blogs
│   ├── Liked Blogs
│   ├── Bookmarked Blogs
│   └── Favourites Collection
│
└── Create Blog
    ├── Title Input
    ├── Content Editor (Markdown/Rich Text)
    ├── Category Selector
    ├── Tag Input (multi-select)
    └── Cover Image Upload
```

### 8.3 API Integration Notes
- **Base URL:** `http://127.0.0.1:8000/` (development)
- **API Route:** `/api/` for blog endpoints
- **Auth Routes:** Root paths (e.g., `/login/`, `/signup/`)
- **Token Storage:** localStorage → Include in all protected requests
- **Image Serving:** Images at `/media/blogs/` automatically served

---

## 9. CONFIGURATION & SETUP

### 9.1 Environment Setup
```bash
# Create virtual environment
python -m venv blog_env

# Activate
source blog_env/bin/activate  # Linux/Mac
blog_env\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
# Starts at http://127.0.0.1:8000/
```

### 9.2 Database Migrations
```bash
# Make migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# View migration status
python manage.py showmigrations
```

### 9.3 Media File Handling
```python
# In settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Frontend upload:
# Use multipart/form-data with file field
# Backend auto-saves to media/blogs/
```

### 9.4 Production Checklist
- [ ] Set `DEBUG = False`
- [ ] Use strong `SECRET_KEY` (environment variable)
- [ ] Configure `ALLOWED_HOSTS` with domain
- [ ] Set `CORS_ALLOWED_ORIGINS` to specific frontend URL
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set up static file serving (whitenoise/nginx)
- [ ] Configure media file serving (S3/CloudStorage)
- [ ] Enable HTTPS
- [ ] Set up logging and error tracking

---

## 10. INTERVIEW TALKING POINTS

### 10.1 Architecture & Design Decisions

**Q: Why did you choose Django + DRF?**

Django provides a robust ORM with built-in admin panel for testing. DRF makes it trivial to build REST APIs with serialization, authentication, and permission handling. Built-in token authentication simplifies frontend integration.

**Q: How is the database structured?**

Core Model: Blog with author, content, timestamps. Interactions: ManyToMany relationships for likes, stars, bookmarks allow efficient querying. Tags: Dynamic creation supports flexible content discovery. Favourites: Separate model for explicit collections.

**Q: Why separate "stars" from "favourites"?**

Different use cases: Likes are quick reactions, bookmarks are for reading later. Favourites is an explicit collection system. This separation allows more granular user preference tracking.

---

### 10.2 API Design

**Q: How does filtering work?**

Query parameters enable flexible filtering:
- `?search=X` performs case-insensitive search across 4 fields
- `?category=X` filters by exact category match
- Filters are composable: `?search=X&category=Y`

Implemented using Django ORM's Q objects for OR logic.

**Q: How do you handle like/bookmark toggling?**

POST endpoint checks if user already in the relation:
```python
if user in blog.likes.all():
    blog.likes.remove(user)  # Unlike
else:
    blog.likes.add(user)     # Like
```

Returns updated count for instant UI feedback.

**Q: What's the authentication flow?**

1. Signup: Create user → Auto-login not needed
2. Login: Authenticate username/password → Generate/retrieve token
3. Storage: Client saves token in localStorage
4. Protected Requests: Include `Authorization: Token <key>` header

DRF handles validation and permission checking automatically.

---

### 10.3 Frontend Integration

**Q: How would you handle API calls on the frontend?**

```javascript
// Example: Get blogs with category filter
fetch('http://127.0.0.1:8000/api/blogs/?category=Tech')
  .then(r => r.json())
  .then(blogs => updateUI(blogs))

// Example: Like a blog
fetch('http://127.0.0.1:8000/api/blogs/1/like/', {
  method: 'POST',
  headers: {
    'Authorization': `Token ${localStorage.getItem('token')}`
  }
})
  .then(r => r.json())
  .then(data => updateLikeCount(data.like_count))
```

**Q: How do you handle token storage and authentication?**

Store token in localStorage after login:
```javascript
// Login
const token = response.token;
localStorage.setItem('authToken', token);

// Protected requests
const headers = {
  'Authorization': `Token ${localStorage.getItem('authToken')}`
};
fetch(url, { headers })
```

---

### 10.4 Scalability & Performance

**Q: How would you optimize for scale?**

- Database: Migrate to PostgreSQL with proper indexing on (user_id, blog_id) for M2M
- Caching: Redis for frequently accessed blogs/tags
- Pagination: Add limit/offset to GET /blogs/
- Search: Implement full-text search with Elasticsearch
- Images: CDN (CloudFront/Cloudflare) for media files
- API: Implement rate limiting to prevent abuse

**Q: Any N+1 query problems?**

Potential issue: Getting liked_blogs with `.all()` might hit database multiple times.

Solution:
```python
# Use select_related/prefetch_related
queryset = Blog.objects.prefetch_related('user', 'tags', 'likes')
```

---

### 10.5 Security Considerations

**Q: How would you secure this in production?**

- [ ] HTTPS enforced (`SECURE_SSL_REDIRECT = True`)
- [ ] CSRF protection (Django default, enabled)
- [ ] Password validation (Django's built-in validators)
- [ ] SQL injection: Protected by ORM (parameterized queries)
- [ ] Rate limiting on auth endpoints (prevent brute force)
- [ ] CORS properly configured (not `ALLOW_ALL_ORIGINS`)
- [ ] Admin panel access restricted and logged

**Q: Is the current CORS configuration safe?**

No. `CORS_ALLOW_ALL_ORIGINS = True` is for development only.

Production should use:
```python
CORS_ALLOWED_ORIGINS = ['https://yourdomain.com']
```

---

### 10.6 Testing & Debugging

**Q: How would you test the API?**

Unit Tests: Test each view/serializer in isolation
```python
from django.test import TestCase

class BlogTestCase(TestCase):
    def test_blog_creation(self):
        blog = Blog.objects.create(...)
        self.assertEqual(blog.read_time, 5)
```

Integration Tests: Test full API workflows with `APITestCase`

Tools: Postman/curl for manual testing, pytest for automation

**Q: Common issues and debugging?**

- 404 on images: Check `MEDIA_URL` and `MEDIA_ROOT` settings
- CORS errors: Verify `CORS_ALLOWED_ORIGINS`
- 401 on protected endpoints: Check token format: `Token <key>`, not `Bearer`
- 400 on blog creation: Validate category against `CATEGORY_CHOICES`

---

### 10.7 Future Enhancements

**Q: What features would you add?**

1. Comments & Replies: Comment model with nested reactions
2. User Profiles: Profile endpoints with follower/following system
3. Notifications: Real-time updates when blog is liked/commented
4. Draft Saving: Blog status field (draft/published)
5. Edit/Delete Blogs: Views with ownership validation
6. Advanced Search: Full-text search, filters by date range
7. Analytics: View count, trending blogs, user engagement metrics
8. Social Sharing: Generate shareable links with metadata

---

### 10.8 Key Code Snippets for Interview

**Serializer with Read-Only Fields:**
```python
class BlogSerializer(serializers.ModelSerializer):
    read_time = serializers.ReadOnlyField()
    like_count = serializers.SerializerMethodField()
    author_username = serializers.ReadOnlyField(source='user.username')
    
    def get_like_count(self, obj):
        return obj.likes.count()
```

**Search with Multiple Fields:**
```python
search_query = request.query_params.get('search', None)
if search_query:
    queryset = queryset.filter(
        Q(title__icontains=search_query) | 
        Q(content__icontains=search_query) |
        Q(category__icontains=search_query) |
        Q(tags__name__icontains=search_query)
    ).distinct()
```

**Token Authentication View:**
```python
class LoginAPIView(APIView):
    def post(self, request):
        user = authenticate(
            username=request.data.get('username'),
            password=request.data.get('password')
        )
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'username': user.username})
```

---

## SUMMARY TABLE

| Aspect | Details |
|--------|---------|
| **Total Endpoints** | 12 major endpoints |
| **Models** | 4 (User, Blog, Tag, Favourites) |
| **Relations** | 5 ManyToMany, 3 ForeignKey |
| **Categories** | 6 (Culture, Travel, Food, Business, Tech, Life) |
| **Authentication** | Token-based (DRF) |
| **Database** | SQLite (dev), PostgreSQL (prod-ready) |
| **API Format** | REST with JSON |
| **Major Libraries** | Django 5.2, DRF 3.16, Pillow, CORS-headers |
| **Frontend Framework** | React 18+ with Vite |

---

## QUICK REFERENCE URLs

```
Development Server: http://127.0.0.1:8000/

Blog Operations:
  GET    /api/blogs/              Get all blogs (filterable)
  POST   /api/blogs/              Create blog
  GET    /api/blogs/{id}/         Get blog details
  POST   /api/blogs/{id}/like/    Toggle like
  POST   /api/blogs/{id}/star/    Toggle star
  POST   /api/blogs/{id}/bookmark/ Toggle bookmark

Auth:
  POST   /signup/                 Create account
  POST   /login/                  Get auth token

Collections:
  GET    /likedblogs/             Get user's liked blogs
  GET    /bookmarkedblogs/        Get user's bookmarked blogs
  POST   /favourite/{id}/         Toggle favourite
  GET    /favblogs/               Get user's favourites
```

---

**This documentation covers everything needed for a comprehensive interview discussion about the Blogging Site project!**