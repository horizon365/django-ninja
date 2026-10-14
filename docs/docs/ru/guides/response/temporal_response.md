---
comments: true
---
# Настройка ответа

Иногда вам захочется изменить ответ непосредственно перед его отправкой, например, чтобы добавить заголовок или изменить cookie.

Для этого просто объявите аргумент функции с типом `HttpResponse`:

```python
from django.http import HttpRequest, HttpResponse

@api.get("/cookie/")
def feed_cookiemonster(request: HttpRequest, response: HttpResponse):
    # Set a cookie.
    response.set_cookie("cookie", "delicious")
    # Set a header.
    response["X-Cookiemonster"] = "blue"
    return {"cookiemonster_happy": True}
```


## Временный объект ответа

Этот объект ответа используется в качестве основы для всех ответов, создаваемых Django Ninja, включая ответы с ошибками.
Если объект Django `HttpResponse` возвращается операцией напрямую, то этот объект *не* используется.

Очевидно, что этот объект ответа ещё не будет содержать контента, но он устанавливает `content_type` (хотя вы, вероятно, не захотите его менять).

`status_code` будет переопределён на основе возвращаемого значения (по умолчанию 200 или код статуса, если возвращается кортеж из двух элементов).


## Изменение базового объекта ответа

Вы можете изменить этот временный объект ответа, переопределив метод `NinjaAPI.create_temporal_response`.

```python
    def create_temporal_response(self, request: HttpRequest) -> HttpResponse:
        response = super().create_temporal_response(request)
        # Do your magic here...
        return response
```

!!! done

    Переходите к следующей главе! **[Генерация схем из моделей Django](django-pydantic.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
