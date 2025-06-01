# GitHub-like Django Repositories App

This is a mini GitHub-like web application built with Django. It allows you to manage repositories, commits, issues, comments, and pull requests.

## Features
### Core Functionality
- **User Authentication**  
  - Sign up (`/accounts/signup/`), login, logout (Django’s built-in auth)  
  - Admin site for superuser management

- **Repositories**  
  - **CRUD**: create, list, detail, update & delete your own repos  
  - Unique per-user names (no duplicates under the same owner)  
  - **Search**: filter by name via a simple GET form

- **Commits**  
  - **CRUD**: add, view, edit & delete commits in a repository  
  - **Date-range filter**: show only commits between two dates  
  - Detail page shows hash, message, author & timestamp

- **Issues**  
  - **CRUD**: open, view, edit & close issues on a repo  
  - **Labels**: color-coded labels (many-to-many)  
  - **Comments**: threaded comments under each issue

- **Pull Requests**  
  - **CRUD** + **Merge** button (mark `is_merged=True`)  
  - Fields: title, description, source/target branch, labels  
  - List, detail & merge flow

### REST API
- **JSON endpoints** for repositories:  
  - `GET /api/repos/` → list of repos  
  - `GET /api/repos/<pk>/` → single repo detail  
- Ready to extend to other models

### UI & UX
- **Bootstrap 5** responsive layout  
- **Breadcrumb** navigation on every page  
- **Consistent templates**: list, form, detail & delete  
- Flash messages & redirects for smooth workflow

### Admin Interface
- All models registered in Django Admin:
  - **Repository**, **Commit**, **Issue**, **Comment**, **PullRequest**  
  - **Label** – create/edit color-coded labels here  
- Full CRUD for all models at `/admin/`


### Architecture & Code
- **6+ Django models** with FK and M2M relations  
- **12+ function-based views** and matching URL patterns  
- **12+ templates** under `templates/repos_app/`  
- **6+ forms**: ModelForms for repos/commits/issues/PRs + signup & filter forms  
- `@login_required` on all user-specific views

### Extras
- Date filtering implemented as a standalone form  
- Self-registration immediately logs you in  
- JSON API tested with `curl`  
- Clean project structure (`repos/`, `repos_app/`, `templates/`, `static/`)  


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

