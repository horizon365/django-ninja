---
comments: true
---
# Добро пожаловать в Django Ninja 1.0


Чтобы начать, установите последнюю версию следующей командой:
```
pip install -U django-ninja
```

django-ninja v1 совместим с Python 3.7 и выше.


Серия Django Ninja 0.x по-прежнему поддерживается, но будет получать только обновления безопасности и исправления критических ошибок.


✨ Что нового в Django Ninja 1.0

## Поддержка Pydantic2

Pydantic версии 2 переписан на Rust и включает множество улучшений и возможностей, таких как:

 - Более безопасные типы.
 - Лучшая расширяемость.
 - Более высокая производительность.

По результатам наших тестов средний проект может получить в среднем около 10% прироста производительности, а в некоторых граничных сценариях парсинга/сериализации можно получить ускорение в 4 раза.
С другой стороны, это вносит критические изменения — pydantic 1 и 2 не полностью совместимы — но мы постарались сделать этот переход максимально простым.
Так что если вы использовали класс 'Schema', миграция на ninja v1 должна быть straightforward. В остальных случаях следуйте [pydantic migration guide](https://pydantic.com.cn/migration/)


Некоторые новые возможности, предоставляемые pydantic2

### pydantic context

Pydantic теперь поддерживает контекст во время валидации и сериализации, а Django Ninja передаёт объект "request" в процессе обработки запросов и ответов.
```Python hl_lines="6 7"
class Payload(Schema):
    id: int
    name: str
    request_path: str

    @staticmethod
    def resolve_request_path(data, context):
        request = context["request"]
        return request.get_full_path()

```

На этапе формирования ответа в контекст также передаётся "response_code".

## Schema.Meta

Pydantic объявил класс BaseModel.Config устаревшим. Однако, чтобы оставаться согласованными со всеми остальными частями Django, мы ввели класс "Meta" для ModelSchema — он работает аналогично Django ModelForms:
```Python hl_lines="2 4"
class TxItem(ModelSchema):
    class Meta:
        model = Transaction
        fields = ["id", "account", "amount", "timestamp"]

```

(Класс "Config" по-прежнему поддерживается, но теперь объявлен устаревшим)


## Более короткий/чистый синтаксис параметров

```python
@api.post('/some')
def some_form(request, username: Form[str], password: Form[str]):
    return True
```

вместо

```python
@api.post('/some')
def some_form(request, username: str = Form(...), password: str = Form(...)):
    return True
```

или

```python
@api.post('/some')
def some_form(request, data: Form[AuthSchema]):
    return True
```


вместо

```python
@api.post('/some')
def some_form(request, data: AuthSchema = Form(...)):
    return True
```



а также все возможности автодополнения в вашем редакторе.


С другой стороны, **старый синтаксис по-прежнему поддерживается**, так что вы сможете без усилий перенести свой проект на последнюю версию django-ninja.


#### + Annotated

typing.Annotated теперь также поддерживается:

```Python
@api.get("/annotated")
def annotated(request, data: Annotated[SomeData, Form()]):
    return {"data": data.dict()}

```


## Поддержка async-аутентификации

Асинхронные аутентификаторы наконец-то поддерживаются. Всё, что нужно сделать, — добавить `async` в ваш метод `authenticate`:

```Python
class Auth(HttpBearer):
    async def authenticate(self, request, token):
        await asyncio.sleep(1)
        if token == "secret":
            return token

```


## Изменённое поведение CSRF


`csrf=True` больше не требуется, если вы используете аутентификацию на основе cookies. Вместо этого защита CSRF включается автоматически. Это также позволяет смешивать аутентификаторы с защитой CSRF и другие методы, не требующие cookies:

```Python
api = NinjaAPI(auth=[django_auth, Auth()])
```


## Документация

Просмотрщик документации теперь настраиваемый и подключаемый. По умолчанию django-ninja поставляется со Swagger и Redoc:
```Python
from ninja import NinjaAPI, Redoc, Swagger


# use redoc
api = NinjaAPI(docs=Redoc()))

# use swagger:
api = NinjaAPI(docs=Swagger())

# set configuration for swagger:
api = NinjaAPI(docs=Swagger({"persistAuthorization": True}))
```

Теперь пользователи могут создавать собственные просмотрщики документации, создавая подкласс класса `DocsBase`.

## Router

add_router поддерживает строковые пути:

```Python
api = NinjaAPI()


api.add_router('/app1', 'myproject.app1.router')
api.add_router('/app2', 'myproject.app2.router')
api.add_router('/app3', 'myproject.app3.router')
api.add_router('/app4', 'myproject.app4.router')
api.add_router('/app5', 'myproject.app5.router')
```


## Декораторы

Когда django-ninja декорирует представление с помощью .get/.post и т.д., он оборачивает результат функции (в большинстве случаев это не HttpResponse, а некий сериализуемый объект), поэтому это вряд ли будет работать с некоторыми встроенными или сторонними декораторами, например:
```python hl_lines="4"
from django.views.decorators.cache import cache_page

@api.get("/test")
@cache_page(5) # <----- will not work!
def test_view(request):
    return {"some": "Complex data"}
```
Этот пример работать не будет.

Теперь django-ninja представляет декоратор decorate_view, позволяющий внедрять декораторы, работающие с http-ответами:
```python hl_lines="1 4"
from ninja.decorators import decorate_view

@api.get("/test")
@decorate_view(cache_page(5))
def test_view(request):
    return str(datetime.now())
```


## Пагинация

Метод `paginate_queryset` теперь принимает объект `request`


#### Обратно несовместимые изменения
 - resolve_xxx(self, ...) - поддержка разрешения (self) объявлена устаревшей в пользу встроенной функциональности pydantic.
 - pydantic v1 больше не поддерживается
 - python 3.6 больше не поддерживается

Кстати — если вам нравится этот проект, и вы ещё не поставили ему звезду на GitHub — пожалуйста, сделайте это! [github star](img/github-star.png)

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
