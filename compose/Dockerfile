FROM python:3.8

ENV PYTHONUNBUFFERED 1

# Install Python and Package Libraries
RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean
RUN apt-get install -y \
    # psycopg2 dependencies
    gcc python3-dev musl-dev \
    # Pillow dependencies
    tk-dev tcl-dev \
    # Translations dependencies
    gettext \
    # https://docs.djangoproject.com/en/dev/ref/django-admin/#dbshell
    postgresql-client

COPY requirements.txt /requirements/requirements.txt
RUN pip install -r /requirements/requirements.txt

COPY ./compose/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

WORKDIR /BodyMeasureControl

ENTRYPOINT ["/entrypoint"]