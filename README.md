# Дипломная работа Foodgram
![example workflow](https://github.com/walera43/foodgram-project-react/actions/workflows/foodgram_workflow.yaml/badge.svg)
[Пример проекта](http://178.154.193.47/)

Тестовый пользователь:
- Логин: test@test.com
- Пароль: test1337
____
Foodgram - сервис на которым вы можете делиться своими рецептами с окружающими!
____
## Установка проекта

Для начала нужно склонировать проект к себе.
1. Создаем файл .env с следующим содержанием:
```
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=****** # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД 
```

2. После с помощью *Docker* через терминал в корневой папке проекта. Развернуть проект следующей командой.

```sh
docker-compose up -d --build 
```

Сборка может занять некоторое время, по окончании работы docker-compose сообщит, что контейнеры собраны и запущены.
3. После нужно провести первичную миграцию для базы данных YaMDb.
```
docker-compose exec web python manage.py migrate --noinput
```
*  _Если данный способ автоматически не произвел миграции, то придется провести вручную. Следующими командами:_
```
docker-compose exec backend python manage.py makemigrations users
docker-compose exec backend python manage.py makemigrations recipes
docker-compose exec backend python manage.py migrate --noinput
```
4. Так же создаем **суперпользователя** для пользования админ-панелью Django.
```
docker-compose exec web python manage.py createsuperuser
```
5. Собираем статику для правильного отображения Admin панели:
```
docker-compose exec web python manage.py collectstatic --no-input
```
6. Заполняем базу данных предустановленными значениями
```
docker-compose exec web python loaddata db.json
```

Теперь проект доступен по адресу http://127.0.0.1/.
Зайдите на http://127.0.0.1/admin/ и убедитесь, что страница отображается полностью: статика подгрузилась.
Авторизуйтесь под аккаунтом суперпользователя и убедитесь, что миграции прошли успешно.
_Для остановки проекта можете использовать_:
```
docker-compose down
```
___
