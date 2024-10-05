# Генерация данных

Можно подкручивать range и ids связей. Расширим скрипт при появлении новых моделей

## Дамп бд

- Стопаем контейнер

- Создаем дамп

```shell
docker cp ./db_dump.dump db_container:./db_dump.dump
```

- Копируем на локальную тачку

```shell
docker cp db_container:./db_dump.dump .
```

- Удаляем volume

```shell
docker volume rm hr-monitor-6146_postgres_data
```

## Загрузка дампа в бд

- Запускаем контейнер

- Копируем дамп в контейнер

```shell
docker cp ./db_dump.dump db_container:./db_dump.dump
```

- Восстанавливаем
- 
```shell
docker exec -t db_container pg_restore -U srv_hr_monitor_adm -d hr_monitor -c ./db_dump.dump
```