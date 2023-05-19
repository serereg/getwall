FROM python:3.10.11-buster

ENV PYTHONUNBUFFERED=1

RUN pip install poetry>=1.1.13 \
    && poetry config virtualenvs.create false

WORKDIR /getwall

COPY ["pyproject.toml", "poetry.lock", "/getwall/"]

RUN poetry install --no-root --no-interaction

COPY . /getwall/

CMD ["uvicorn", "getwall.application:app", "--host", "0.0.0.0", "--reload"]
