FROM python:3.12.3

RUN apt-get update && \
    apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY . .

ENV POETRY_VIRTUALENVS_CREATE=false
RUN poetry install --no-root --no-dev

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["python", "-m", "src"]
