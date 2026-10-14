---
comments: true
---
# Аутентификация

## Введение

**Django Ninja** предоставляет несколько инструментов, которые помогут вам обрабатывать аутентификацию и авторизацию легко, быстро и стандартным способом, без необходимости изучать <a href="https://swagger.io/docs/specification/authentication/" target="_blank">все спецификации безопасности</a>.

Основная идея в том, что при описании API-операции вы можете определить объект аутентификации.
```python hl_lines="2 7"
{!./src/tutorial/authentication/code001.py!}
```

В этом примере клиент сможет вызвать метод `pets`, только если использует аутентификацию сессий Django (которая по умолчанию основана на cookie), иначе будет возвращена ошибка HTTP-401.
Если вы хотите авторизовывать только суперпользователей, вы можете использовать вместо этого `from ninja.security import django_auth_superuser`.
## Автоматическая схема OpenAPI

Вот пример, где клиенту нужно передать заголовок, чтобы пройти аутентификацию:

`Authorization: Bearer supersecret`

```python hl_lines="4 5 6 7 10"
{!./src/tutorial/authentication/bearer01.py!}
```

Теперь перейдите к документации <a href="http://localhost:8000/api/docs" target="_blank">http://localhost:8000/api/docs</a>.


![Swagger UI Auth](../img/auth-swagger-ui.png)

Теперь при нажатии кнопки **Authorize** вам будет предложено ввести ваш токен аутентификации.

![Swagger UI Auth](../img/auth-swagger-ui-prompt.png)

При выполнении тестового вызова каждый запрос будет передавать заголовок авторизации.

## Глобальная аутентификация

Если вам нужно защитить **все** методы вашего API, вы можете передать аргумент `auth` в конструктор `NinjaAPI`:


```python hl_lines="11 19"
from ninja import NinjaAPI, Form
from ninja.security import HttpBearer


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token


api = NinjaAPI(auth=GlobalAuth())

# @api.get(...)
# def ...

# @api.post(...)
# def ...
```

А если вам нужно переопределить некоторые из методов, вы можете сделать это снова на уровне операции, передав аргумент `auth`. В этом примере аутентификация будет отключена для операции `/token`:
```python hl_lines="19"
{!./src/tutorial/authentication/global01.py!}
```

## Доступные варианты аутентификации

### Пользовательская функция


Аргумент "`auth=`" принимает любой callable. **NinjaAPI** выполнит аутентификацию только тогда, когда callable вернёт значение, которое является **истинным** (преобразуется в булево `True`). Это возвращаемое значение будет присвоено атрибуту `request.auth`.

```python hl_lines="1 2 3 6"
{!./src/tutorial/authentication/code002.py!}
```


### API-ключи

Некоторые API используют API-ключи для авторизации. API-ключ — это токен, который клиент предоставляет при вызове API, чтобы идентифицировать себя. Ключ можно отправить в строке запроса:
```
GET /something?api_key=abcdef12345
```

Или в заголовке запроса:

```
GET /something HTTP/1.1
X-API-Key: abcdef12345
```

Или в cookie:

```
GET /something HTTP/1.1
Cookie: X-API-KEY=abcdef12345
```

**Django Ninja** поставляется со встроенными классами, которые помогут вам обработать эти ситуации.


#### В Query

```python hl_lines="1 2 5 6 7 8 9 10 11 12"
{!./src/tutorial/authentication/apikey01.py!}
```

В этом примере мы получаем токен из `GET['api_key']` и находим соответствующий `Client` в базе данных. Экземпляр Client будет установлен как атрибут `request.auth`.

Примечание: **`param_name`** — это имя GET-параметра, который будет проверяться. Если оно не задано, используется значение по умолчанию `"key"`.


#### В Header

```python hl_lines="1 4"
{!./src/tutorial/authentication/apikey02.py!}
```

#### В Cookie

```python hl_lines="1 4"
{!./src/tutorial/authentication/apikey03.py!}
```



### HTTP Bearer

```python hl_lines="1 4 5 6 7"
{!./src/tutorial/authentication/bearer01.py!}
```

### HTTP Basic-аутентификация

```python hl_lines="1 4 5 6 7"
{!./src/tutorial/authentication/basic01.py!}
```


## Несколько аутентификаторов

Аргумент **`auth`** также позволяет передать несколько аутентификаторов:

```python hl_lines="18"
{!./src/tutorial/authentication/multiple01.py!}
```

В этом случае **Django Ninja** сначала проверит API-ключ из `GET`, и если он не задан или недействителен, проверит ключ `header`.
Если оба недействительны, в ответ будет выброшена ошибка аутентификации.


## Аутентификация роутера

Используйте аргумент `auth` на роутере, чтобы применить аутентификатор ко всем операциям, объявленным в нём:

```python
api.add_router("/events/", events_router, auth=BasicAuth())
```

Или через конструктор роутера
```python
router = Router(auth=BasicAuth())
```


## Пользовательские исключения

Выброс исключения, у которого есть обработчик исключений, вернёт ответ этого обработчика таким же образом, как и для операции:

```python hl_lines="1 4"
{!./src/tutorial/authentication/bearer02.py!}
```


## Асинхронная аутентификация

**Django Ninja** имеет базовую поддержку асинхронной аутентификации. Хотя классы аутентификации по умолчанию не совместимы с async, вы всё равно можете определить свой собственный асинхронный callable для аутентификации и передать его через `auth`.

```python
async def async_auth(request):
    ...


@api.get("/pets", auth=async_auth)
def pets(request):
    ...
```


Для получения дополнительной информации смотрите [Обработка ошибок](errors.md) .

!!! success

    Перейдите к следующему разделу **[Тестирование](testing.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
