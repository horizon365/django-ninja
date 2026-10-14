---
comments: true
---
# Параметры пути

Вы можете объявлять «параметры» пути, используя тот же синтаксис, что и в форматированных строках Python (который, к счастью, также совпадает с <a href="https://swagger.io/docs/specification/describing-parameters/#path-parameters" target="_blank">параметрами пути OpenAPI</a>):

```python hl_lines="1 2"
{!./src/tutorial/path/code01.py!}
```

Значение параметра пути `item_id` будет передано в вашу функцию в качестве аргумента `item_id`.

Итак, если вы запустите этот пример и перейдёте по адресу <a href="http://localhost:8000/api/items/foo" target="_blank">http://localhost:8000/api/items/foo</a>, вы увидите такой ответ:

```JSON
{"item_id":"foo"}
```


### Параметры пути с типами

Вы можете объявить тип параметра пути, используя стандартные аннотации типов Python в вашей функции:

```python hl_lines="2"
{!./src/tutorial/path/code02.py!}
```

В этом случае `item_id` объявлен как **`int`**. Это даёт вам поддержку редактора и линтера для проверки ошибок, автодополнения кода и т. д.

Если вы запустите этот код в браузере по адресу <a href="http://localhost:8000/api/items/3" target="_blank">http://localhost:8000/api/items/3</a>, вы увидите такой ответ:
```JSON
{"item_id":3}
```

!!! tip
    Обратите внимание, что значение, которое получает (и возвращает) ваша функция, — это **3**, как Python `int`, а не строка `"3"`.
    Таким образом, с помощью лишь этого объявления типа **Django Ninja** обеспечивает автоматический «разбор» запроса и его валидацию.



### Валидация данных

С другой стороны, если вы зайдёте в браузере по адресу <a href="http://localhost:8000/api/items/foo" target="_blank">http://localhost:8000/api/items/foo</a> <small>*(`"foo"` — не int)*</small>, вы увидите HTTP-ошибку следующего вида:

```JSON hl_lines="8"
{
    "detail": [
        {
            "loc": [
                "path",
                "item_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```


### Конвертеры пути Django

Вы можете использовать [конвертеры пути Django](https://docs.djangoproject.com/en/stable/topics/http/urls/#path-converters),
чтобы облегчить разбор пути:

```python hl_lines="1"
@api.get("/items/{int:item_id}")
def read_item(request, item_id):
    return {"item_id": item_id}
```

В этом случае `item_id` будет разобран как **`int`**. Если `item_id` не является корректным `int`, URL не совпадёт.
(Например, если ни один другой маршрут не совпадёт, будет возвращён ответ 404 Not Found.)

!!! tip
    Обратите внимание: поскольку **Django Ninja** использует тип `str` по умолчанию для неаннотированных параметров, значение, которое получает (и возвращает) приведённая выше функция, — это `"3"`,
    как Python `str`, а не целое число **3**. Чтобы получить `int`, просто объявите `item_id` с аннотацией типа `int` в определении функции, как обычно:

    ```python hl_lines="2"
    @api.get("/items/{int:item_id}")
    def read_item(request, item_id:int):
        return {"item_id": item_id}
    ```
 
#### Параметры пути со слэшами

Конвертер `path` в Django позволяет обрабатывать параметры, похожие на путь:

```python hl_lines="1"
@api.get('/dir/{path:value}')
def someview(request, value: str):
    return value
```
Вы можете запросить эту операцию по адресу `/dir/some/path/with-slashes`, и ваш `value` будет равен `some/path/with-slashes`

### Несколько параметров

Вы можете передавать в `path` сколько угодно переменных — просто не забудьте использовать уникальные имена и не забудьте использовать те же имена в аргументах вашей функции.

```python
@api.get("/events/{year}/{month}/{day}")
def events(request, year: int, month: int, day: int):
    return {"date": [year, month, day]}
```


### Использование схемы

Вы также можете использовать схему для инкапсуляции взаимозависимых параметров пути (и их групповой валидации):


```python hl_lines="1 2  5 6 7 8 9 10 11 15"
{!./src/tutorial/path/code010.py!}
```

!!! note
    Обратите внимание, что здесь мы используем подсказку источника `Path`, чтобы **Django Ninja** знал, что эта схема будет применяться к параметрам пути.

### Документация

Теперь, открыв в браузере <a href="http://localhost:8000/api/docs" target="_blank">http://localhost:8000/api/docs</a>, вы увидите автоматическую интерактивную документацию API.
![Django Ninja Swagger](../../img/tutorial-path-swagger.png)

!!! done

    Переходите к следующей главе! **[Параметры запроса](query-params.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
