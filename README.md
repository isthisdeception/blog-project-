# Django Blog Project

🌐 **Live Demo**: [https://blog-project-d9p7.onrender.com/](https://blog-project-d9p7.onrender.com/)

A full-featured Django blog application with user authentication, post management, and a responsive Bootstrap 5 UI.

---

## Features

- 📝 Create, read, update, and delete blog posts
- 👤 User registration, login, and logout
- 🔐 Password reset via email
- 💬 Comment system on posts
- 🎨 Responsive design using Bootstrap 5 & Crispy Forms
- 🗂️ Pagination, search, and sidebar widgets
- 🐘 PostgreSQL support (production-ready on Render)
- 📦 Static & media file handling via WhiteNoise

---

## Tech Stack

| Layer       | Technology                         |
|-------------|------------------------------------|
| Framework   | Django 5.x                         |
| Frontend    | Bootstrap 5, Crispy Forms           |
| Database    | SQLite (dev) / PostgreSQL (prod)    |
| Deployment  | Render                              |
| Static Files| WhiteNoise                           |
| Python      | 3.14                                |

---

## Installation (Local Development)

```powershell
# 1. Clone the repo
git clone <your-repo-url>
cd blog_project

# 2. Create & activate virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows
# source .venv/bin/activate    # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create a superuser (optional)
python manage.py createsuperuser

# 6. Start the dev server
python manage.py runserver
```

Visit **http://127.0.0.1:8000/** in your browser.

---

## Deployment on Render

1. Push the code to GitHub
2. Create a new **Web Service** on [Render](https://render.com)
3. Connect your repository
4. Set the following **Environment Variables**:

   | Variable         | Value                                         |
   |------------------|-----------------------------------------------|
   | `SECRET_KEY`     | `<a-secure-random-string>`                     |
   | `DATABASE_URL`   | `<your-postgresql-connection-string>`          |
   | `ALLOWED_HOSTS`  | `blog-project-d9p7.onrender.com,localhost,127.0.0.1` |
   | `DEBUG`          | `False`                                        |

5. Deploy — Render will handle `pip install`, `collectstatic`, and `migrate` automatically

---

## Project Structure

```
├── blog_project/       # Django project settings
├── blog/               # Blog app (posts, comments)
├── accounts/           # User authentication app
├── pages/              # Static pages app
├── templates/          # Shared HTML templates
├── static/             # Shared static files (CSS, JS, images)
├── media/              # User-uploaded media files
├── requirements.txt    # Python dependencies
└── manage.py           # Django management script
```

---

## License

MIT
