---
comments: true
---
## Введение
О JWT я слышал давно, но никогда не использовал его на практике. Недавно, изучая протокол возобновляемой загрузки tus, я добрался до уровня hooks-http с целью выполнять аутентификацию во время загрузки файлов. Естественно, я вспомнил о пакете `django-ninja-jwt`. Я думал, что всё будет просто, но, прочитав [китайскую документацию](https://django-ninja.cn/django-ninja-jwt/), обнаружил, что это не просто просто — это до удивительного минималистично.

## Начало работы

Согласно руководству, достаточно установить `dango-ninja-jwt` и `django-ninja-extra`, затем заменить `NinjaAPI` на `njaExtraAPI` — и это занимает всего одну строку.

```python
api.register_controllers(NinjaJWTDefaultController)
```

Честно говоря, это ставит в тупик.

Подождите — давайте сначала взглянем на документацию. Появляются три новых эндпоинта: `pair`, `refresh` и `verify`.
![JWT swagger UI token](../img/jwt-token.png)
Обратите внимание на значок замка в правом верхнем углу — он пригодится нам позже. Он появляется только когда вы используете функцию `JWTAuth`.

### pair
Первый — это эндпоинт `pair`. Он означает, что после того, как вы предоставите имя пользователя и пароль, он вернёт токены аутентификации и refresh-токены.
Формат тела запроса следующий:
```json
{
  "password": "string",
  "username": "string"
}
```
Примечание: здесь `username` располагается ниже, что немного отличается от того, что вы могли бы предположить.
После нажатия Execute вы получите примерно следующее:
```json
{
  "data": {
    "username": "lyq",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MzE0NzU2NCwiaWF0IjoxNzQyNTQyNzY0LCJqdGkiOiI4MTZmMzg2YWYwNmY0NmVhOWY1YzlkMDJjYzQxZjFkOCIsInVzZXJfaWQiOjF9.G-mTefGtP-cTXWVrxAsqXGGKnZ1442jw67ilvTY5gcQ",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyNjI5MTY0LCJpYXQiOjE3NDI1NDI3NjQsImp0aSI6IjdiMGY1Y2Y5NTVlZDRiMzQ5M2M3MmY4NzJmNDdkMzUxIiwidXNlcl9pZCI6MX0.JO9PxVA-rX6TPo9Db00eOuOorThjgX3nTjBT-CuOh90"
  }
}
```
### refresh
Показанный выше токен `access` можно использовать для аутентификации, но по умолчанию у него ограниченное время жизни. Токен `refresh` имеет большее время жизни, чем `access`, и используется для получения нового токена `access` после истечения срока действия предыдущего.
После обновления предыдущий токен `access` становится недействительным.

Теперь вы можете скопировать `access` в значок замка в правом верхнем углу. Так каждый эндпоинт на текущей странице сможет его использовать — это удобно при отладке.
### verify
Вы можете перейти к третьему эндпоинту, `verify`, чтобы проверить, действителен ли токен `access`.

В целом, `django-ninja-jwt` просто создаёт для вас три эндпоинта, упрощая получение, обновление и проверку токенов.

## Кастомизация
Одних этих трёх эндпоинтов недостаточно — как минимум, нам нужно добавить аутентификацию к нашим собственным конкретным эндпоинтам.
Здесь вам понадобится `JWTAuth`; только после его использования появится значок замка.
```python
from ninja_jwt.authentication import JWTAuth
@route.get('/some', auth=JWTAuth())
def some_endpoint(request):
    """Convenient for showing the auth button on the docs page"""
    return request.auth.username
```
И у эндпоинта `some` появится собственный отдельный значок замка.
![JWT swagger UI token custom](../img/jwt-token-custom.png)
Для указанного выше эндпоинта `some`, если аутентификация проходит успешно, он возвращает имя пользователя текущего вошедшего пользователя. Если нет — возвращает ответ 401.
Backend-разработчикам нужно сказать команде frontend, чтобы они отправляли это значение — пусть они перейдут в раздел [pair](#pair), чтобы получить его, и периодически обращаются к [refresh](#refresh), чтобы его обновить.

### Настройка времени жизни токенов

```python
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),  # Access token lifetime
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),  # Refresh token lifetime
    'AUTH_HEADER_TYPES': ('Bearer',),
}

```
### Дополнительная кастомизация
Если использования `@route.get('/some', auth=JWTAuth())` в вашем ninja-маршруте недостаточно, вы можете вызвать `authenticate` внутри функции.

```python
@route.get('/some')
def some_endpoint(request):
    auth = JWTAuth()
    # If it fails, a 401 is raised internally
    if auth.authenticate(request, token):
        return request.auth.username

```
Токен `token`, упомянутый выше, нужно извлечь из объекта `request` самостоятельно.
