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
Переименуйте  `.env1`. в  `.env`  
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