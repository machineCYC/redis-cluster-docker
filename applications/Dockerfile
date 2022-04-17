FROM python:3.8

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
COPY ./app /code/app

RUN apt-get update

RUN pip install --upgrade pip install -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]