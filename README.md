# NeuroHack HR Monitor

Проект выполняемый в рамках хакатона T1 Хакатон в Нижнем Новгороде

https://codenrock.com/contests/impulse-hackt1-nizhny-novgorod#/
--

Платформа для мониторинга качества работы рекрутеров

93.183.90.209

Если не доступно, то не успели поднять

В планах зарезолвить на домен neurohack.tech

## Требования для запуска

- docker
- docker compose


## Запуск

```
docker compose up --build -d
```

Сервис будет доступен на localhost на 80 порту

API будет запущено на localhost:8000

Возможна долгая установка npm install, мы заметили это при деплое, если проходим в финал, то обязательно исправим


## Наполнение БД сгенерированными значениями

curl http://localhost:8000/init_random_db


### Swagger:

http://localhost:8000/docs 


# Используемые технологии

- python 3.12
- FastAPI
- sqlAlchemy
- alembic
- pydantic
- postgreSQL
- nginx
- js
- Vue.js
