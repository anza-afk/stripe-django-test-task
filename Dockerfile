
FROM python:3.10.8-alpine

WORKDIR /usr/src/invoice_generator

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/invoice_generator/entrypoint.sh
RUN chmod +x /usr/src/invoice_generator/entrypoint.sh
COPY . .
RUN mkdir /usr/src/invoice_generator/static
RUN python invoice_generator/manage.py collectstatic --noinput