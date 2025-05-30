# GitHub-like Django Repositories App

This is a mini GitHub-like web application built with Django. It allows you to manage repositories, commits, issues, comments, and pull requests.

## Features

- User authentication (login, logout, sign up)
- CRUD for Repositories, Commits, Issues, Comments, Pull Requests
- REST API endpoints for repositories
- Bootstrap 5-based responsive UI
- Admin interface for all models

## Prerequisites

- Python 3.8+
- pip

## Setup

1. Unzip the file
2. run: python3 -m venv venv
3. source the venv: source venv/bin/activate
4. pip install -r requirements.txt
5. Configure SECRET_KEY:
Edit repos/settings.py and replace the placeholder SECRET_KEY = '…'
with a securely generated one, např.: python -c "import secrets; print(secrets.token_urlsafe(50))"

5. Migration and superuser creation: python manage.py migrate
python manage.py createsuperuser   # pro pristup do /admin/
6.  launch the server: python manage.py runserver
7. for FE open: http://127.0.0.1:8000/ or http://127.0.0.1:8000/repos/
8. for admin open: http://127.0.0.1:8000/admin/

