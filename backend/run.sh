#!/bin/bash
echo 'Starting backend'
alembic upgrade head
python -m src