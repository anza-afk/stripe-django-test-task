# stripe-django-test-task

Запуск проекта с помощью Docker:

Создать .env файл в директории
C:\Projects\stripe-django-test-task\invoice_generator\invoice_generator
и заполнить его по примеру .env.example

docker-compose -f docker-compose.yml up -d --build
docker-compose -f docker-compose.yml exec web python manage.py migrate --noinput
docker-compose -f docker-compose.yml exec web python manage.py collectstatic --no-input --clear
docker-compose -f docker-compose.yml exec web python manage.py createsuperuser

endpoint /item/<id> ведёт на оплату заказа одной item из бд
endpoint /order/<id> ведёт на оплату заранее созданного заказа из бд
endpoint /create_order ведёт на создание заказа из нескольких вещей
(оплата нескольких item сработает только, если item в одной валюте)