FROM python:3.10-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY ./requirements-lock.txt /code/
RUN pip install -r requirements-lock.txt

COPY . /code/

CMD ["uvicorn", "getwall.application:app", "--host", "0.0.0.0", "--reload"]
