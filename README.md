# django-Ecommerce
### Install venv for store dependency for project
- python -m venv venv
### Activate venv
#### In cmd.exe
- venv\Scripts\activate.bat
#### In PowerShell
- venv\Scripts\Activate.ps1
### Install Django from requirements.txt
- pip install -r requirements.txt
### create model for Database
- python manage.py makemigrateions 
- and then python manage.py migrate
### Create user for login to admin page
- python manage.py createsuperuser
### run server
- python manage.py runserver