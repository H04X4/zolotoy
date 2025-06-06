Order Management
Django-проект для управления заказами через админку с возможностью загрузки Excel-файлов.

Создайте базу:
psql -U postgres -c "CREATE DATABASE order_management;"

Обновите settings.py:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'order_management',
        'USER': 'postgres',
        'PASSWORD': 'ваш_пароль',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

Примените миграции:
python manage.py makemigrations
python manage.py migrate

Создайте суперпользователя:
python manage.py createsuperuser

Запустите сервер:
python manage.py runserver

Админка доступна по адресу: http://127.0.0.1:8000/admin/






