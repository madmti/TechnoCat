FROM arm32v7/python:3.11.6-alpine3.18

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apk update \
    && apk add --no-cache gcc cargo rust build-base openssl-dev musl-dev docker-compose python3-dev libffi-dev \
    && pip install --upgrade pip 

COPY ./requirements.txt ./

RUN pip install -r requirements.txt
COPY ./ ./

CMD [ "sh", "entrypoint.sh" ]