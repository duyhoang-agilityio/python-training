# Employee Management System

This is a Django-based project to manage employees, departments, contacts, and projects. The project demonstrates the use of database modeling, relationships, migrations, custom querysets, and other Django features.

---

## **Folder Structure**
```plaintext
employee_management/
│
├── core/                          # Core app containing models, views, and commands
│   ├── management/commands/       # Custom Django management commands
│   │   └── combine_full_name.py   # Command to combine first_name and last_name
│   ├── migrations/                # Database migrations
│   ├── __init__.py                # App initializer
│   ├── admin.py                   # Admin configurations
│   ├── apps.py                    # App configuration
│   ├── models.py                  # Django models
│   ├── tests.py                   # Unit tests
│   ├── views.py                   # Views for the app
│
├── employee_management/           # Project settings
│   ├── __init__.py
│   ├── settings.py                # Project settings
│   ├── urls.py                    # Project URL configurations
│   ├── wsgi.py                    # WSGI entry point for the app
│
├── env/                           # Virtual environment (not included in Git)
├── db.sqlite3                     # SQLite database
├── manage.py                      # Django management tool
├── .gitignore                     # Git ignore file
└── README.md                      # Project documentation
```

---

## **Steps to Run the Project**

### 1. **Clone the Repository**
```bash
git clone git@gitlab.asoft-python.com:duy.hoang/python_training.git
cd employee_management
```

### 2. **Set Up a Virtual Environment**
Create and activate a virtual environment:
```bash
python -m venv env
source env/bin/activate       # For MacOS/Linux
```

### 3. **Install Dependencies**
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### 4. **Run Migrations**
Initialize the database by applying migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. **Seed Initial Data**
Run the custom management command to add initial data:
```bash
python manage.py seed
```

### 6. **Start the Development Server**
Start the Django development server:
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser to access the app.

---

## **Configuration**

### **Deployment Gunicorn**

1. **Install Gunicorn**
   ```bash
   python -m pip install gunicorn
   ```

2. **Run Gunicorn**
   ```bash
   gunicorn --bind 0.0.0.0:8000 employee_management.wsgi:application
   ```

---

## **Unit Testing**
Run unit tests using the Django test framework:
```bash
python manage.py test
```

---

## **Features**
- Database modeling with relationships between employees, departments, contacts, and projects.
- Custom management commands for automating tasks.
- QuerySet filters and aggregations for advanced querying.
- Separate settings for development, testing, and production.
- Deployment ready with Gunicorn.