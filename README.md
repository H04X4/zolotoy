# 📦 Order Management

**Django-проект для управления заказами через админку с возможностью загрузки Excel-файлов.**

---

## 🚀 Быстрый старт

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/yourusername/order-management.git
cd order-management
```

### 2. Создайте базу данных PostgreSQL

```bash
psql -U postgres -c "CREATE DATABASE order_management;"
```

### 3. Обновите настройки подключения в `settings.py`

```python
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
```

### 4. Примените миграции

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Создайте суперпользователя

```bash
python manage.py createsuperuser
```

### 6. Запустите сервер разработки

```bash
python manage.py runserver
```

🛠️ Админка будет доступна по адресу:  
[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- Файл artcles.xlsx для тестов  
---

## 📁 Загрузка Excel-файлов

В админке можно загружать Excel-файлы с артикулами (название, остатки, цены и т.п.) для автоматического импорта данных в систему.


## ✅ Возможности

- Загрузка Excel с артикулами
- Работа с заказами в админке
- Комментарии, пересчет сумм
