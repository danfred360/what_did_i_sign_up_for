FROM python:3.10

RUN mkdir /var/log/what-did-i-sign-up-for
RUN useradd -ms /bin/bash api

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/api
COPY ./logging_config.json /code/api/logging_config.json

RUN chown -R api:api /code
RUN chown -R api:api /var/log/what-did-i-sign-up-for

USER api

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80", "--log-config", "api/logging_config.json"]