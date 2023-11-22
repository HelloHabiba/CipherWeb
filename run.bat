@echo off
REM Create a virtual environment (optional but recommended)
python -m venv venv
call venv\Scripts\activate

REM Install Django and other requirements
pip install django
pip install -r requirements.txt

REM Make migrations and migrate
python manage.py makemigrations
python manage.py migrate

REM Run the Django development server
python manage.py runserver

REM Deactivate the virtual environment
call venv\Scripts\deactivate

echo.
echo Django application is now running.
pause
