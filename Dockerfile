FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install poetry

RUN poetry install

COPY . /app/

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "main:app"]