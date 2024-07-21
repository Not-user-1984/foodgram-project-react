
## Проект **Foodgram** 

![example workflow](https://github.com/Not-user-1984/foodgram-project-react/actions/workflows/djangorest.yml/badge.svg)

![python version](https://img.shields.io/badge/Python-3.10-green)
![django version](https://img.shields.io/badge/Django-4.1-green)
![Docker version](https://img.shields.io/badge/Docker-4.15-green)
![Djangorestframework version](https://img.shields.io/badge/Djangorestframework-3.14-green)
![PyJWT version](https://img.shields.io/badge/PyJWT-2.6-green)
![gunicornversion](https://img.shields.io/badge/gunicorn-20.01-green)
![gunicornversion](https://img.shields.io/badge/nginx-1.19.3-green)


#### Проект доступен по адресу

[http://picipe.ddns.net/recipes](http://picipe.ddns.net/recipes)

[Документация Api](http://picipe.ddns.net/api/docs/)
<hr>

## Описание

Foodgram - продуктовый помощник для публикации рецептов. Mожно подписываться на рецепты других пользователей, а также на понравившихся авторов, добавлять рецепты в избранное, а также в список покупок, чтобы затем скачать список.
<br> 
<hr>
<details>
<summary><strong>Запуск в Docker контейнерах</strong></summary>
<br>
Установите Docker.

Склонировать проект с git
```
git@github.com:Not-user-1984/foodgram-project-react.git
```

В директории infra/ необходимо создать файл .env:
```
cd infra
touch .env
```

В котором требуется указать переменные окружения, пример:
```
SECRET_KEY=django-insecure-9zls+ggt68%6z^(4xmyunp8v#2wtd!hw%0f47r2ioo4$bvi72n
DB_ENGINE=django.db.backends.postgresql 
DB_NAME=postgres 
POSTGRES_USER=postgres 
POSTGRES_PASSWORD=postgres 
DB_HOST=db
DB_PORT=5432
```

В директории infra/, в файле nginx.conf измените адрес(ip/домен), необходимо указать адрес вашего сервера.

Запустите docker compose
```
docker-compose up -d --build
```

Примените миграции
```

docker-compose exec backendpython manage.py makemigrations
docker-compose exec backend python manage.py migrate
```

Загрузите ингредиенты
```
docker-compose exec backend python manage.py ingred_load
```

Создайте суперпользователя
```
docker-compose exec backend python manage.py createsuperuser
```

Далее соберите статику
```
docker-compose exec backend python manage.py collectstatic --noinput
```
</details>
<br>
<hr>

<details>
<summary><strong> Работа сайта</strong></summary>
<br>

### Уровни доступа пользователей:
Гость (неавторизованный пользователь)
Авторизованный пользователь
Администратор

### Что могут делать неавторизованные пользователи
- Создать аккаунт.
- Просматривать рецепты на главной.
- Просматривать отдельные страницы рецептов.
- Просматривать страницы пользователей.
- Фильтровать рецепты по тегам.

### Что могут делать авторизованные пользователи
- Входить в систему под своим логином и паролем.
- Выходить из системы (разлогиниваться).
- Менять свой пароль.
- Создавать/редактировать/удалять собственные рецепты
- Просматривать рецепты на главной.
- Просматривать страницы пользователей.
- Просматривать отдельные страницы рецептов.
- Фильтровать рецепты по тегам.
- Работать с персональным списком избранного: добавлять в него рецепты или удалять их, просматривать свою страницу избранных рецептов.
- Работать с персональным списком покупок: добавлять/удалять любые рецепты, выгружать файл со количеством необходимых ингридиентов для рецептов из списка покупок.
- Подписываться на публикации авторов рецептов и отменять подписку, просматривать свою страницу подписок.

### Что может делать администратор- 
Администратор обладает всеми правами авторизованного пользователя. 
Плюс к этому он может:
- изменять пароль любого пользователя,
- создавать/блокировать/удалять аккаунты пользователей,
- редактировать/удалять любые рецепты,
- добавлять/удалять/редактировать ингредиенты.
- добавлять/удалять/редактировать теги.

</details>

<br>
<hr>
<details>

<br>
<summary><strong> API Примеры запросов: </strong></summary>
<br>

Примеры запросов:
Для регистрации пользователя, необходимо отправить POST запрос на адрес:
```
http://http://picipe.ddns.net/api/users/
```
Тело запроса
```
{
    "email": "vova_not_is@yandex.ru",
    "username": "vova_bomba23",
    "first_name": "Вова",
    "last_name": "Путкин",
    "password": "baiden_lox"
}
```

Для получения токена, следует отправить POST запрос на адрес:
```
http://http://picipe.ddns.net/api/auth/token/login/
```
Тело запроса
```
{
    "password": "baiden_lox",
    "email": "vova_not_is@yandex.ru"
}
```

Получить список рецептов можно отправив GET запрос на эндпоинт:
```
http://http://picipe.ddns.net/api/recipes/
```

Чтобы создать новый рецепт нужно отправить POST запрос на адрес(Доступно только с токеном):
```
http://http://picipe.ddns.net/api/recipes/
```

Тело запроса
```
{
    "ingredients": [
        {
        "id": 1123,
        "amount": 10
        }
    ],
    "tags": [
        1,
        2
    ],
    "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
    "name": "string",
    "text": "string",
    "cooking_time": 1
}
```

</details>

<br>
<br>
<br>
<hr>

#### **Разработчик**:
[Дима Плужников](https://github.com/Not-user-1984)

#### **Tg**:
@DmitryPluzhnikov