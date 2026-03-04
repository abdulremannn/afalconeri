# AFalconeri Technologies — Django Web Application

## Setup Instructions

### 1. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Apply Migrations
```bash
python manage.py migrate
```

### 4. Collect Static Files
```bash
python manage.py collectstatic
```

### 5. Run Development Server
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

## Project Structure
```
afalconeri/
├── manage.py
├── requirements.txt
├── README.md
├── afalconeri/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/
│   ├── __init__.py
│   ├── apps.py
│   ├── urls.py
│   ├── views.py
│   ├── forms.py
│   └── templates/
│       └── core/
│           ├── base.html
│           ├── home.html
│           ├── systems.html
│           ├── capabilities.html
│           ├── about.html
│           └── contact.html
└── static/
    ├── css/
    │   └── main.css
    ├── js/
    │   └── main.js
    └── images/
```

## Pages
- `/` — Home
- `/systems/` — Platform Registry
- `/capabilities/` — Technical Capabilities
- `/about/` — Company About
- `/contact/` — Secure Contact Form

## Environment Variables (.env)
```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost 127.0.0.1
```
