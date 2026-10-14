
#### Требования
- Python >= 3.6
- Django >= 2.1
- Django-Ninja >= 0.16.1
- Django-Ninja-Extra >= 0.11.0

Это официально поддерживаемые версии Python и пакетов. Другие версии также могут работать. Вы можете свободно изменить конфигурацию tox и посмотреть, что возможно.

## Установка

Ninja JWT можно установить через pip:

    pip install django-ninja-jwt

Кроме того, вам нужно зарегистрировать контроллер `NinjaJWTDefaultController` в вашем Django-Ninja API.

```python
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)

```
`NinjaJWTDefaultController` поставляется с тремя маршрутами: `obtain_token`, `refresh_token` и `verify_token`.
Он представляет собой комбинацию двух подклассов: `TokenVerificationController` и `TokenObtainPairController`.
Если вы хотите настроить эти маршруты, вы можете унаследоваться от этих контроллеров и изменить их реализацию.

```python
from ninja_extra import api_controller
from ninja_jwt.controller import TokenObtainPairController

@api_controller('token', tags=['Auth'])
class MyCustomController(TokenObtainPairController):
    """Only obtain token and refresh token"""
...
api.register_controllers(MyCustomController)
```

Если вы хотите использовать локализацию/перевод, просто добавьте `ninja_jwt` в `INSTALLED_APPS`.

```python
INSTALLED_APPS = [
    ...
    'ninja_jwt',
    ...
]
```

## Использование

Чтобы убедиться, что Ninja JWT работает, вы можете отправить несколько тестовых запросов с помощью curl:

``` {.sourceCode .bash}
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": "davidattenborough", "password": "boatymcboatface"}' \
  http://localhost:8000/api/token/pair

...
{
  "access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNDU2LCJqdGkiOiJmZDJmOWQ1ZTFhN2M0MmU4OTQ5MzVlMzYyYmNhOGJjYSJ9.NHlztMGER7UADHZJlxNG0WSi22a2KaYSfd1S-AuT7lU",
  "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImNvbGRfc3R1ZmYiOiLimIMiLCJleHAiOjIzNDU2NywianRpIjoiZGUxMmY0ZTY3MDY4NDI3ODg5ZjE1YWMyNzcwZGEwNTEifQ.aEoAYkSJjoWH1boshQAaTkf8G3yn0kapko6HFRt7Rh4"
}
```

Вы можете использовать возвращённый access-токен для подтверждения аутентификации при обращении к защищённым представлениям:

``` {.sourceCode .bash}
curl \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNDU2LCJqdGkiOiJmZDJmOWQ1ZTFhN2M0MmU4OTQ5MzVlMzYyYmNhOGJjYSJ9.NHlztMGER7UADHZJlxNG0WSi22a2KaYSfd1S-AuT7lU" \
  http://localhost:8000/api/some-protected-view/
```

Когда этот недолговечный access-токен истечёт, вы можете использовать более долговечный refresh-токен, чтобы получить новый access-токен:

``` {.sourceCode .bash}
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImNvbGRfc3R1ZmYiOiLimIMiLCJleHAiOjIzNDU2NywianRpIjoiZGUxMmY0ZTY3MDY4NDI3ODg5ZjE1YWMyNzcwZGEwNTEifQ.aEoAYkSJjoWH1boshQAaTkf8G3yn0kapko6HFRt7Rh4"}' \
  http://localhost:8000/api/token/refresh/

...
{"access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXN...", "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVm..."}
```

Криптографические зависимости (необязательно)
-------------------------------------

Если вы планируете кодировать или декодировать токены с использованием определённых алгоритмов цифровой подписи (т.е. RSA и ECDSA; см. PyJWT для других алгоритмов),
вам потребуется установить библиотеку cryptography_. Её можно установить явно или как обязательный элемент зависимостей `django-ninja-jwt`:

    pip install django-ninja-jwt[crypto]

При использовании файла зависимостей проекта `Ninja JWT` рекомендуется формат `django-ninja-jwt[crypto]`,
потому что отдельная строка требования `cryptography` впоследствии может быть ошибочно принята за неиспользуемую зависимость и удалена.
[cryptography](https://cryptography.io)

!!! success

    Перейдите к следующей главе **[Аутентификация маршрутов](auth_integration.md)**.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
