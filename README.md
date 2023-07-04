# solution-factory-test-task
Тестовое задание для Solution Factory. API для рассылки 

# Start project without docker
### Подготовка виртуального окружения
```
pip install pipenv #если ранее не установлен
pipenv sync 
pipenv shell
```
### Запуск проекта
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Запуск Celery
```
celery -A config worker -l info
```
### Запуск Celery Beat
```
celery -A config beat -l info
```
***Важно!*** Для корректной работы Celery Beat необходимо запустить Celery Worker
***Celery и Celery Beat можно запустить одной командой:***
```
celery -A config worker --beat --loglevel=info
```
### Запуск Flower
Flower - это веб-интерфейс для мониторинга и управления задачами Celery. Его запуск необязателен.
Доступен по адресу http://127.0.0.1:5555/
```
celery -A config flower
```

### Запуск RabbitMQ
Стандартные логины и пароли для RabbitMQ: guest/guest
Доступен по адресу http://127.0.0.1:15672/#/
```
 docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management 
```

# Start project with docker
```
docker-compose up --build
```

# API
После запуска проекта API будет доступно по адресу
<br>http://127.0.0.1:8000/docs либо 
<br>http://127.0.0.1:8000/redoc
### Авторизация
Для авторизации используется админ аккаунт Django с параметрами username и password.
Аккаунт администратора можно создать через консоль командой
```
python manage.py createsuperuser
```
Аккаунт пользователя можно создать через Web интерфейс статистики по адресу: 
<br>http://127.0.0.1:8000/account/register/
