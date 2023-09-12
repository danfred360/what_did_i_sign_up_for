FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./api /code/app

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]