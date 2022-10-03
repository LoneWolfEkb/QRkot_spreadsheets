# QRKot
Учебный проект. API приложения для Благотворительного фонда поддержки котиков QRKot. 
Его назначение — сбор и распределение пожертвований между различными проектами

## Использование
Склонируйте репозиторий  
Создайте виртуальное окружение 
```
python -m venv venv
```
Активируйте виртуальное окружение  
Установите зависимости 
```
pip install -r requirements.txt
```

Создайте файл .env с настройками, к примеру:

```
APP_TITLE=Благотворительный фонд котиков
DESCRIPTION=Сбор пожертвований на нужды хвостатых
DATABASE_URL=your_database
SECRET=your_secret
FIRST_SUPERUSER_EMAIL
FIRST_SUPERUSER_PASSWORD=
EMAIL=
TYPE=service_account
PROJECT_ID=
PRIVATE_KEY_ID=
PRIVATE_KEY=
CLIENT_EMAIL=
CLIENT_ID=
AUTH_URI=
TOKEN_URI=
AUTH_PROVIDER_X509_CERT_URL=
CLIENT_X509_CERT_URL=
```

Примените миграции
```
alembic upgrade head
```
Запустите сервер из корневой папки проекта
```
uvicorn app.main:app --reload
```
При первом запуске приложения будет создан суперюзер, с регистрационными данными из `.env`  

Документация и web интервейс API будет доступен по адресу: [http://localhost:8000/docs](http://localhost:8000/docs)

## Автор
- [Турхан Михаил](https://github.com/LoneWolfEkb)
