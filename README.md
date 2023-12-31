# Тестовое задание.

Написать микросервис уведомления пользователей. 

Микросервис должен представлять из себя RestAPI сервер, который позволяет создавать запись уведомления в документе пользователя в MongoDB, отправлять email, а так же предоставлять листинг уведомлений из документа пользователя.

Уведомления пользователей должны храниться в поле в документе пользователя и их максимальное кол-во должно быть ограничено (лимит можно установить произвольный)

При тестировании отправки Email отпраляйте key от создаваемого уведомления.

#### Пример уведомления в документе пользователя

```json
{
    "id": "some_notification_id",
    "timestamp": 1698138241,
    "is_new": false,
    "user_id": "638f394d4b7243fc0399ea67",
    "key": "new_message",
    "target_id": "0399ea67638f394d4b7243fc",
    "data": {
        "some_field": "some_value"
    },
},
```

Для теста в случае отсутствия пользователя следует создать новый профиль с email, который задан через параметры.

## Переменные окружения, через которые конфигурируется сервис

- PORT - порт на котором будет работать приложение
- EMAIL - тестовый email
- DB_URI - строка для подключения к mongoDB
- SMTP_HOST - хост smtp сервера
- SMTP_PORT - порт smtp сервера
- SMTP_LOGIN - логин пользователя
- SMTP_PASSWORD - пароль пользователя
- SMTP_EMAIL - email с которого будет отправлено сообщение
- SMTP_NAME - Имя отображаемое у получателя письма

## API Handlers: 

### [POST] /create создает новое уведомление.

#### Тело запроса:

- user_id - строка на 24 символа (является ObjectID документа пользователя которому отправляется уведомление)
- target_id - строка на 24 символа (является ObjectID документа сущности, к которой относится уведомление) (Может отсутствовать)
- key - ключ уведомления enum
    - registration (Только отправит пользователю Email)
    - new_message (только создаст запись в документе пользователя)
    - new_post (только создаст запись в документе пользователя)
    - new_login (Создаст запись в документе пользователя и отправит email)
- data - произвольный объект из пар ключ/значение (Может отсутствовать)

#### Пример тела запроса:

```json
{
    "user_id": "638f394d4b7243fc0399ea67",
    "key": "registration",
}
```

#### Пример ответа

HTTP 201 Created

```json
{
    "success": true,
}
```

### [GET] /list производит листинг уведомлений пользователя.

#### query params
- user_id [string] - идентификатор пользователя
- skip [int] - кол-во уведомлений, которые следует пропустить
- limit [int] - кол-во уведомлений которые следует вернуть

#### Пример ответа

HTTP 200 Ok

```json
{
    "success": true,
    "data": {
        "elements": 23, // всего уведомлений
        "new": 12, // Кол-во непрочитанных уведомлений
        "request": {
            "user_id": "638f394d4b7243fc0399ea67",
            "skip": 0,
            "limit": 10,
        }
        "list": [
            {
                "id": "some_notification_id",
                "timestamp": 1698138241,
                "is_new": false,
                "user_id": "638f394d4b7243fc0399ea67",
                "key": "new_message",
                "target_id": "0399ea67638f394d4b7243fc",
                "data": {
                    "some_field": "some_value"
                },
            },
            ...
        ]
    }
}
```

#### [POST] /read создает отметку о прочтении уведомления.

#### query params
- user_id [string] - идентификатор пользователя
- notification_id [string] - Идентификатор уведомления

#### Пример ответа

HTTP 200 Ok

```json
{
    "success": true,
}
```

## На ваше усмотрение

Вам позволено решать указанные выше задачи тем способом, который вы сочтете наиболее подходящим. Кратко опишите свой подход в решении задач в Readme файле в репозитории.

## Результат выполнения задания

Данное задание будет считаться выполненным при условии размещения кода и Dockerfile'a в репозитории на github.com.

Прошу отправить результат выполнения задания на Email:
papkovda@me.com

в теме письма укажите: "Тестовое задание"

в теле письма приложите ссылку на свой профиль на hh.ru и репозиторий на github с выполненым тестовым заданием.


# Решение задания

Для реализации данного проекта использован следующий стек технологий:
- Python 3.10
- FastAPI 
- Pydentic
- MongoDB
- PyMongo
- Motor

В ходе реализации задания было создано приложение использующее асинхронное выполнение функционала.

Архитектура проекта выполнена с разделением функциональных частей приложения по различным модулям.

## Запуск приложения
Запуск приложения возможен в двух вариантах на локальной машине и с помощью инструментов контейнеризации Docker Compose.

## Локальный запуск приложения

Для запуска проекта на локальной машине необходимо выполнить следующие шаги:
1. Скопировать код проекта на локальную машину.
2. Создать тестовую базу данных 
3. Создать и активировать виртуальное окружение выполнив команды в терминале:
```commandline
$ python3 -m venv venv
$ source venv/bin/activate
```
4. Установить зависимости проекта с помощью команд в терминале:
```commandline
$ pip install -r requirements.txt
```
5. Создать файл .env содержащий чувствительные данные для запуска приложения. В качестве основы содержания файла нужно использовать файл template.env. И записать в него значения необходимых данных для запуска сервера приложения, соединения с базой данных и использования почтового сервера.
6. Запустить север приложения выполнив команду в терминале:
```commandline
$ uvicorn --reload main:app
```
7. Для просмотра документации по API в браузере перейти по URL адресу http://127.0.0.1:8000/docs - для просмотра документации Swagger 
 или по URL адресу http://127.0.0.1:8000/redoc - для просмотра документации redoc.
8. Для выполнения запросов к API приложения можно использовать страницу swagger в браузере или выполнять запросы с помощью Postman.

## Запуск приложения в контейнерах Docker Compose

1.  Для запуска приложения с помощью Docker Compose необходимо создать образы контейнеров выполнив команду в терминале:
```commandline
$ docker compose build
```
2. Создать и запустить контейнеры выполнив команду в терминале:
```commandline
$ docker compose up -d
```
3. Приложение будет доступно по URL адресу http://0.0.0.0:8000

