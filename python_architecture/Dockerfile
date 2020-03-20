FROM python:3.8-alpine

# install systems' stuff to be able to run postges packages
RUN apk add --no-cache --virtual .build-deps gcc postgresql-dev musl-dev python3-dev
RUN apk add libpq

# install the packages
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

# cleanup the installation
RUN apk del --no-cache .build-deps

# copy the code
RUN mkdir -p /src
COPY src/ /src/

# install the package in editable mode
RUN pip install -e /src
COPY tests/ /tests/

# TODO(Mihai): replace with gunicorn
# Something safer than port 80
WORKDIR /src
ENV FLASK_APP=allocation/entrypoints/flask_app.py FLASK_DEBUG=1 PYTHONUNBUFFERED=1
CMD flask run --host=0.0.0.0 --port=80