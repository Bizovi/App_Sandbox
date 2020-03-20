FROM python:3.8-alpine

RUN apk add --no-cache --virtual .build-deps gcc postgresql-dev musl-dev python3-dev
RUN apk add libpq

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

RUN apk del --no-cache .build-deps

# oh Bloody Mary, what a hack :(:(
RUN mkdir -p /code
COPY *.py /code
WORKDIR /code

# quite a catastrophe: no gunicorn, port 80 ready for breaches
ENV FLASK_APP=entrypoints/flask_app.py FLASK_DEBUG=1 PYTHONUNBUFFERED=1
CMD flask run --host=0.0.0.0 --port=80