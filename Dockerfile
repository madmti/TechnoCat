FROM python:3.11.6-alpine3.17

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./requirements.txt ./

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY ./ ./

CMD [ "sh", "entrypoint.sh" ]