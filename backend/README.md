# HR Monitor Backend

## backend/.env file example

```commandline
POSTGRES_DB = db_name
POSTGRES_USER = db_name_user
POSTGRES_PASSWORD = db_name_password
```

## run

```shell
docker compose up
```

## alembic

```shell
alembic revision --autogenerate -m "update tables"
alembic upgrade head
```
