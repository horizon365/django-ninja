---
comments: true
---
# Обработка ошибок

**Django Ninja** позволяет устанавливать пользовательские обработчики исключений, чтобы контролировать, как возвращаются ответы при возникновении ошибок или обрабатываемых исключений.

## Пользовательские обработчики исключений

Предположим, вы строите API, который зависит от некоторого внешнего сервиса, спроектированного быть недоступным в определённые моменты. Вы можете обработать эту ошибку и вернуть клиенту какой-нибудь дружелюбный ответ (попросив его зайти позже) вместо выброса стандартной ошибки 500 при возникновении исключения.
Для этого нужно:

 - 1) Создать некоторое исключение (или использовать существующее)
 - 2) Использовать декоратор api.exception_handler


Пример:


```python hl_lines="9 10"
api = NinjaAPI()

class ServiceUnavailableError(Exception):
    pass


# initializing handler

@api.exception_handler(ServiceUnavailableError)
def service_unavailable(request, exc):
    return api.create_response(
        request,
        {"message": "Please retry later"},
        status=503,
    )


# some logic that throws exception

@api.get("/service")
def some_operation(request):
    if random.choice([True, False]):
        raise ServiceUnavailableError()
    return {"message": "Hello"}

```

Функция-обработчик исключения принимает 2 аргумента:

 - **request** - HTTP-запрос Django
 - **exc** - само исключение

Функция должна вернуть HTTP-ответ

## Переопределение обработчиков исключений по умолчанию

По умолчанию **Django Ninja** инициализирует следующие обработчики исключений:


#### `ninja.errors.AuthenticationError`

Выбрасывается, когда данные аутентификации недействительны

#### `ninja.errors.ValidationError`

Выбрасывается, когда данные запроса не проходят валидацию

#### `ninja.errors.HttpError`

Используется для выброса HTTP-ошибки с кодом статуса из любого места кода
#### `django.http.Http404`
 
Стандартное исключение 404 в Django (можно возвращать, например, с помощью get_object_or_404)
#### `Exception`
 
Любое другое исключение, не обработанное приложением.
Стандартное поведение
 
  - **Если `settings.DEBUG` равен `True`** - возвращает traceback в виде простого текста (удобно при отладке в консоли или Swagger UI)
  - **иначе** - используется стандартный механизм обработки исключений Django (логирование ошибок, отправка писем администраторам ADMINS)


### Переопределение стандартных обработчиков

Если вам нужно изменить стандартный вывод ошибок валидации — переопределите обработчик исключения ValidationError:

```python hl_lines="1 4"
from ninja.errors import ValidationError
...

@api.exception_handler(ValidationError)
def validation_errors(request, exc):
    return HttpResponse("Invalid input", status=422)
```


## Выброс HTTP-ответов через исключения

В качестве альтернативы созданию пользовательского исключения и написанию обработчика для него — вы также можете выбросить HTTP-исключение, в результате чего будет возвращён HTTP-ответ с нужным кодом

```python
from ninja.errors import HttpError

@api.get("/some/resource")
def some_operation(request):
    if True:
        raise HttpError(503, "Service Unavailable. Please retry later.")

```
!!! success

    Перейдите к следующему разделу **[Формирование обратных URL](urls.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
