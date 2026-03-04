# 🏥 MediCare HMS — Hospital Management System
### Built with Python · Django · SQLite · Django REST Framework

---

## ⚡ ONE-CLICK SETUP & RUN

```bash
cd hms_project
python setup_and_run.py
```

That's it. Opens at → **http://127.0.0.1:8000/dashboard/**

---

## 📋 MANUAL SETUP (if needed)

```bash
# 1. Install Python packages
pip install -r requirements.txt

# 2. Create database & tables
python manage.py makemigrations
python manage.py migrate

# 3. Create admin user
python manage.py createsuperuser

# 4. Start server
python manage.py runserver
```

---

## 🔑 DEFAULT LOGIN

| Field    | Value     |
|----------|-----------|
| Username | admin     |
| Password | admin123  |

---

## 🌐 URLS

| Page             | URL                                  |
|------------------|--------------------------------------|
| Dashboard        | http://localhost:8000/dashboard/     |
| Patients         | http://localhost:8000/patients/      |
| Visit Records    | http://localhost:8000/visits/        |
| Appointments     | http://localhost:8000/appointments/  |
| Admin Panel      | http://localhost:8000/admin/         |
| REST API Root    | http://localhost:8000/api/           |

---

## 🔌 REST API ENDPOINTS

```
GET/POST    /api/patients/
GET/PUT/DEL /api/patients/{id}/
GET         /api/patients/{id}/visits/
GET         /api/patients/{id}/appointments/
PATCH       /api/patients/{id}/update_status/

GET/POST    /api/visits/
GET/PUT/DEL /api/visits/{id}/
POST        /api/visits/{id}/add_prescription/

GET/POST    /api/appointments/
GET/PUT/DEL /api/appointments/{id}/
PATCH       /api/appointments/{id}/confirm/
PATCH       /api/appointments/{id}/cancel/
PATCH       /api/appointments/{id}/complete/

GET         /api/dashboard-stats/
```

---

## 📦 TECH STACK

- **Backend**: Django 5.0 + Django REST Framework
- **Database**: SQLite (dev) — change to PostgreSQL for production
- **Frontend**: Pure HTML/CSS (no frameworks, no Node.js needed)
- **Auth**: Django built-in auth + admin

---

## 🗂️ PROJECT STRUCTURE

```
hms_project/
├── setup_and_run.py          ← ONE-CLICK SETUP
├── manage.py
├── requirements.txt
├── hms_project/
│   ├── settings.py
│   └── urls.py
├── patients/
│   ├── models.py             ← Patient, VisitRecord, Prescription, Appointment
│   ├── views.py              ← Template views
│   ├── api_views.py          ← REST API ViewSets
│   ├── serializers.py        ← DRF Serializers
│   ├── forms.py              ← Django Forms
│   ├── urls.py               ← Template URL routes
│   └── api_urls.py           ← API URL routes
└── templates/patients/
    ├── base.html             ← Sidebar + topbar layout
    ├── dashboard.html
    ├── patient_list.html
    ├── patient_form.html
    ├── patient_detail.html
    ├── visit_list.html
    ├── visit_form.html
    ├── visit_detail.html
    ├── appointment_list.html
    └── appointment_form.html
```

---

## 🚀 PRODUCTION (PostgreSQL)

In `hms_project/settings.py`, change:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hms_db',
        'USER': 'postgres',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Also set `DEBUG = False` and add your domain to `ALLOWED_HOSTS`.
