---
comments: true
---
# HTTP-методы

## Определение операций

`operation` может быть одним из [HTTP-методов](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods):

- GET (получение)
- POST (отправка)
- PUT (обновление)
- DELETE (удаление)
- PATCH (частичное обновление)

У **Django Ninja** есть декоратор для каждой операции:

```python hl_lines="1 5 9 13 17"
@api.get("/path")
def get_operation(request):
    ...

@api.post("/path")
def post_operation(request):
    ...

@api.put("/path")
def put_operation(request):
    ...

@api.delete("/path")
def delete_operation(request):
    ...

@api.patch("/path")
def patch_operation(request):
    ...
```

Информацию о том, что можно передавать в любой из этих декораторов, смотрите в справочной документации [Параметры операций](../../reference/operations-parameters.md).

## Обработка нескольких методов

Если вам нужно обрабатывать несколько методов для заданного пути одной функцией, вы можете использовать декоратор `api_operation`:

```python hl_lines="1"
@api.api_operation(["POST", "PATCH"], "/path")
def mixed_operation(request):
    ...
```

Эту возможность также можно использовать для реализации других HTTP-методов, для которых нет соответствующего метода **Django Ninja**, например `HEAD` или `OPTIONS`.

```python hl_lines="1"
@api.api_operation(["HEAD", "OPTIONS"], "/path")
def mixed_operation(request):
    ...
```

!!! done

    Переходите к следующей главе! **[Параметры пути](path-params.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
