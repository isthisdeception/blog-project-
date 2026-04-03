#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate

python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()

username = 'admin'
email = 'admin@email.com'
password = 'amdin'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
"
