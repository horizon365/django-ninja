---
comments: true
---
# Параметры запроса

Когда вы объявляете параметры функции, не являющиеся частью параметров пути, они автоматически интерпретируются как параметры «запроса».
```python hl_lines="5"
{!./src/tutorial/query/code01.py!}
```

Чтобы вызвать эту операцию, можно использовать URL следующего вида:

```
http://localhost:8000/api/weapons?offset=0&limit=10
```
По умолчанию все GET-параметры являются строками; когда вы аннотируете параметры функции типами, они будут преобразованы в соответствующий тип и проверены на соответствие.

Те же преимущества, что и для параметров пути, применимы и к параметрам запроса:

- Поддержка редактора (очевидно)
- «Разбор» данных
- Валидация данных
- Автоматическая документация


!!! note
    Если вы не аннотируете ваши параметры, они будут считаться типом `str`

```python hl_lines="2"
@api.get("/weapons")
def list_weapons(request, limit, offset):
    # type(limit) == str
    # type(offset) == str
```

### Значения по умолчанию

Поскольку параметры запроса не являются фиксированной частью пути, они необязательны и могут иметь значения по умолчанию:

```python hl_lines="2"
@api.get("/weapons")
def list_weapons(request, limit: int = 10, offset: int = 0):
    return weapons[offset : offset + limit]
```

В приведённом выше примере мы задали значения по умолчанию `offset=0` и `limit=10`.

Итак, посещение URL:
```
http://localhost:8000/api/weapons
```
будет эквивалентно посещению:
```
http://localhost:8000/api/weapons?offset=0&limit=10
```
Если вы, например, посетите:
```
http://localhost:8000/api/weapons?offset=20
```

Значения параметров в вашей функции будут:

 - `offset=20` (потому что вы задали его в URL)
 - `limit=10` (потому что это значение по умолчанию)


### Обязательные и необязательные параметры

Вы можете объявлять обязательные или необязательные GET-параметры так же, как объявляете параметры Python-функций:

```python hl_lines="5"
{!./src/tutorial/query/code02.py!}
```

В этом случае **Django Ninja** всегда будет проверять параметр `q`, который вы передаёте в GET-запросе, а параметр `offset` является необязательным целым числом.

### Преобразование типов GET-параметров

Объявим несколько параметров с типами:
```python hl_lines="5"
{!./src/tutorial/query/code03.py!}
```
Тип `str` передаётся как есть.

Для типа `bool` все следующие варианты:
```
http://localhost:8000/api/example?b=1
http://localhost:8000/api/example?b=True
http://localhost:8000/api/example?b=true
http://localhost:8000/api/example?b=on
http://localhost:8000/api/example?b=yes
```
или любые другие варианты регистра (заглавные, с заглавной буквы и т. д.), ваша функция увидит,
что параметр `b` имеет булево значение `True`, иначе `False`.

Даты могут быть строками дат и целыми числами (Unix timestamps):

<pre style="font-size: .85em; background-color:rgb(245, 245, 245);">
http://localhost:8000/api/example?d=<strong>1577836800</strong>  # equivalent to 2020-01-01
http://localhost:8000/api/example?d=<strong>2020-01-01</strong>
</pre>


### Использование схемы

Вы также можете использовать схему для инкапсуляции GET-параметров:

```python hl_lines="1 2  5 6 7 8"
{!./src/tutorial/query/code010.py!}
```

Для более сложных сценариев фильтрации обратитесь к разделу [Фильтрация](./filtering.md).

!!! done

    Переходите к следующей главе! **[Тело запроса](body.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
