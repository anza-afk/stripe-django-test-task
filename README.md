# stripe-django-test-task

Клонируем проект:

    git clone https://github.com/anza-afk/stripe-django-test-task.git

## Запуск проекта с помощью Docker:

Создать .env файл в корневой директории и заполнить его по примеру .env.example из корня проекта
(При возможных проблемах - скопировать его в stripe-django-test-task\invoice_generator\invoice_generator)

### Выполнить в корне проекта:

    docker-compose -f docker-compose.yml up -d --build
    docker-compose -f docker-compose.yml exec web python manage.py migrate --noinput
    docker-compose -f docker-compose.yml exec web python manage.py collectstatic --no-input --clear
    docker-compose -f docker-compose.yml exec web python manage.py createsuperuser
    
### Эндпоинты:

endpoint /item/\<id\> ведёт на оплату заказа одной item из бд

endpoint /order/\<id\> ведёт на оплату заранее созданного заказа из бд

endpoint /create_order ведёт на создание заказа из нескольких вещей</br>
*(заказ из нескольких item в разных валютах не пройдёт на этапе оплаты)*
