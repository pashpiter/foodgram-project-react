# Foodgram

[![foodgram_workflow](https://github.com/pashpiter/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)](https://github.com/pashpiter/foodgram-project-react/actions/workflows/foodgram_workflow.yml)

### О чем проект
Портал для создания рецептов, которые потом смогу посмотреть и использовать другие пользователи! 

##### Стек: Python, Django, Django REST, gunicorn, nginx, Docker, Postgresql, Git, Github Actions
***

### Что умеет foodgram
* Создание рецептов
* Изменение рецепта
* Добавление рецепта в избранное
* Подписка на авторов рецепта
* Добавление игредиетов рецепта в корзину, для дальнейшей загрузки файла списка продуктов в текстовом формате
***
### Запуск проекта
Для запуска проекта на сервере необходимо: 
* Клонировать репозиторий
```
git clone https://github.com/pashpiter/foodgram-project-react/
```
* Установить Docker
```
sudo apt install docker.io
```
* Скопируйте на сервер файлы docker-compose.yml, nginx.conf из папки infra
* Для работы с GitHub Actions добавить Secrets в репозиторий
```
SECRET_KEY              # секретный ключ Django проекта
DOCKER_USERNAME         # логин Docker Hub
DOCKER_PASSWORD         # пароль от Docker Hub
HOST                    # публичный IP сервера
USER                    # имя пользователя на сервере
SSH_KEY                 # приватный ssh-ключ
PASSPHRASE              # *если ssh-ключ защищен паролем
TELEGRAM_TO             # ID телеграм-аккаунта для посылки сообщения
TELEGRAM_TOKEN          # токен бота, посылающего сообщение

DB_ENGINE               # django.db.backends.postgresql
DB_NAME                 # Имя базы данных
POSTGRES_USER           # Логин для подключения к Postgres
POSTGRES_PASSWORD       # Пароль для подключения к Postgres
DB_HOST                 # Название контейнера
DB_PORT                 # 5432 (порт по умолчанию)
```
* Запустить docker-compose
```
sudo docker-compose up -d
```
* Выполните миграции в контейнере backend
```
sudo docker-compose exec backend python manage.py migrate
```
* Создайте суперпользователя
```
sudo docker-compose exec backend python manage.py createsuperuser
```
* Соберите статику
```
sudo docker-compose exec backend python manage.py collectstatic
```
* Добавьте ингрдиенты в базу
```
sudo docker-compose exec backend python manage.py ingredients_input
```

### Примеры команд API
* Создание пользователя
```
POST http://<ip_server>/api/users/
{
    "username": "",
    "email": "",
    "first_name": "",
    "last_name": "",
    "password": ""
}
```
* Получение токена
```
POST http://<ip_server>/api/auth/token/login
{
    "email": "",
    "password": ""
}
```
* Создание рецепта
```
POST http://<ip_server>/api/recipes/
{
    "ingredients": [
        {
            "id": 1,
            "amount": 1
        }
    ],
    "tags": [
        1
    ],
    "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
    "text": "String",
    "name": "String",
    "cooking_time": "Num"
}
```
* Получение списка рецептов
```
GET http://<ip_server>/api/recipes/
```
* Добавление рецепта в избранное
```
POST http://<ip_server>/api/recipes/<id_recipe>/favorite/
```
* Добавление рецепта в корзину
```
POST http://<ip_server>/api/recipes/<id_recipe>/shopping_cart/
```
* Получение списка ингредиентов из корзины
```
GET http://<ip_server>/api/recipes/download_shopping_cart
```
* Подписка на автора
```
POST http://<ip_server>/api/users/2/subscribe/
```
***
# Author
## Pavel Drovnin [@pashpiter](http://t.me/pashpiter)
