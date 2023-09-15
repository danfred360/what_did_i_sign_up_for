FROM python:3.10

RUN mkdir /var/log/what-did-i-sign-up-for
RUN useradd -ms /bin/bash auth

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/api

RUN chown -R auth:auth /code
RUN chown -R auth:auth /var/log/what-did-i-sign-up-for

USER auth

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80", "--log-config", "api/logging_config.json"]