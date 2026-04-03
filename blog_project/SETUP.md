# DevBlog — Setup Instructions

A complete modern blog website built with Django, Bootstrap 5, and Django Crispy Forms.

## Quick Start

### 1. Install Required Packages

Open your terminal in the `blog_project` directory and run:

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install Django crispy-bootstrap5 Pillow
```

### 2. Run Migrations

Create the database tables:

```bash
cd blog_project
python manage.py makemigrations
python manage.py migrate
```

### 3. Create a Superuser (for Admin Access)

```bash
python manage.py createsuperuser
```

### 4. (Optional) Seed the Database with Sample Data

For testing, go to `http://localhost:8000/admin/`, log in with your superuser account, and create some sample Categories, Tags, and Posts.

### 5. Start the Development Server

```bash
python manage.py runserver
```

### 6. Visit the Website

Open your browser and go to:
- **Website**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/

---

## Project Structure

```
blog_project/
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
├── SETUP.md                    # This file
├── db.sqlite3                  # SQLite database (created after migrate)
│
├── blog_project/               # Project settings
│   ├── __init__.py
│   ├── settings.py             # Main Django settings
│   ├── urls.py                 # Root URL configuration
│   ├── wsgi.py
│   └── asgi.py
│
├── blog/                       # Core blog app
│   ├── models.py               # Post, Category, Tag, Comment, Like, Newsletter
│   ├── views.py                # All blog views (class-based)
│   ├── forms.py                # Post and comment forms (crispy)
│   ├── urls.py                 # Blog URL routes
│   ├── admin.py                # Admin panel customization
│   ├── context_processors.py   # Sidebar data (recent, popular posts, etc.)
│   └── templates/blog/
│       ├── post_list.html      # Homepage with post cards
│       ├── post_detail.html    # Single post with comments
│       ├── post_form.html      # Create/edit post form
│       ├── post_confirm_delete.html
│       ├── author_posts.html   # All posts by an author
│       ├── category_posts.html # Posts by category
│       ├── tag_posts.html      # Posts by tag
│       ├── _post_card.html     # Reusable post card component
│       ├── _pagination.html    # Pagination component
│       └── _sidebar.html       # Sidebar widget
│
├── accounts/                   # User authentication app
│   ├── models.py               # Profile model (extended user)
│   ├── views.py                # Register, login, logout, profile views
│   ├── forms.py                # Registration and profile forms
│   ├── urls.py                 # Auth URL routes
│   ├── admin.py
│   └── templates/accounts/
│       ├── register.html       # Registration form
│       ├── login.html          # Login form
│       ├── profile.html        # User profile page
│       ├── edit_profile.html   # Edit profile page
│       ├── change_password.html
│       ├── password_reset.html
│       ├── password_reset_done.html
│       ├── password_reset_confirm.html
│       ├── password_reset_complete.html
│       ├── password_reset_email.html
│       └── password_reset_subject.txt
│
├── pages/                      # Static pages app
│   ├── views.py                # About, Contact, Newsletter views
│   ├── urls.py                 # Pages URL routes
│   └── templates/pages/
│       ├── about.html          # About page
│       ├── contact.html        # Contact page with form
│       └── 404.html            # Custom 404 page
│
├── templates/                  # Root templates folder
│   └── base.html               # Base template (navbar + footer)
│
├── static/                     # Static files (CSS, JS)
│   └── css/
│       └── style.css           # Custom styles
│
└── media/                      # User-uploaded media files
    ├── posts/                  # Blog post images
    └── profile_pics/           # User profile pictures
```

---

## Features Implemented

### Authentication
- [x] User registration with styled form
- [x] Login/logout with sessions
- [x] Password reset via email (console backend in dev)
- [x] User profile with picture upload
- [x] Edit profile and change password

### Blog Features
- [x] Create, update, delete posts (author only)
- [x] Rich post detail page with full content
- [x] Post list with pagination
- [x] Category system with post counts
- [x] Tag system with post filtering
- [x] Search posts by title and content
- [x] Like system (AJAX toggle, one per user)
- [x] Comment system with nested replies
- [x] Recent posts sidebar
- [x] Popular posts sidebar (by like count)
- [x] Related posts section
- [x] Author page (all posts by an author)

### UI / Design
- [x] Bootstrap 5 responsive layout
- [x] Sticky navbar with dropdowns
- [x] Hero section on homepage
- [x] Post cards with hover animations
- [x] Dark, modern footer
- [x] Beautiful forms with Crispy Forms
- [x] Bootstrap Icons throughout
- [x] Google Fonts (Inter + Merriweather)
- [x] Mobile responsive
- [x] Reusable base template

### Additional Features
- [x] Admin panel customization (colored badges, inline comments)
- [x] SEO-friendly URLs with slugs
- [x] Django messages (success/error alerts)
- [x] Image upload for posts
- [x] Media/static file config
- [x] Custom 404 page
- [x] Newsletter subscription form
- [x] Contact page with form
- [x] About page
- [x] Share buttons (Twitter, Facebook, LinkedIn)

---

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Framework | Django 4.2+ |
| Frontend | Bootstrap 5.3 + Bootstrap Icons |
| Forms | Django Crispy Forms + crispy-bootstrap5 |
| Database | SQLite (dev) |
| Images | Pillow |
| Views | Class-based views (ListView, DetailView, CreateView, etc.) |

---

## Production Checklist

Before deploying to production:

1. **Set DEBUG = False** in `settings.py`
2. **Generate a secure SECRET_KEY** using `django.core.management.utils.get_random_secret_key()`
3. **Set ALLOWED_HOSTS** to your domain(s)
4. **Configure a production email backend** (SendGrid, Mailgun, etc.)
5. **Run `python manage.py collectstatic`** for static files
6. **Use a production database** (PostgreSQL, MySQL)
7. **Set up a WSGI server** (Gunicorn, uWSGI)
8. **Use a reverse proxy** (Nginx, Apache)
9. **Enable HTTPS** (Let's Encrypt)
10. **Configure `MEDIA_ROOT`** to a secure location
