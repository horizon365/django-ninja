---
title: Django Ninja - Быстрый REST-фреймворк для Django
template: home.html
comments: true
---

Django Ninja — это веб-фреймворк для построения API с Django и подсказками типов Python 3.6+.

Основные возможности:

 - **Легок в понимании**: Разработан так, чтобы быть простым в использовании и интуитивным.
 - **Быстрое выполнение**: Благодаря **<a href="https://pydantic.com.cn" target="_blank">Pydantic</a>** и **<a href="guides/async-support/">поддержке async</a>**, он обладает очень высокой производительностью.
 - **Быстрое написание кода**: Django Ninja — это веб-фреймворк для построения API с Django и подсказками типов Python 3.6+.
 - **Основан на стандартах**: Базируется на стандартах: **OpenAPI** (ранее Swagger) и **JSON Schema**.
 - **Дружелюбен к Django**: (очевидно) хорошо интегрируется с ядром Django и ORM.
 - **Готов к продакшену**: Используется несколькими компаниями в реальных проектах (если вы используете Django Ninja и хотите опубликовать свой отзыв, напишите на ppr.vitaly@gmail.com).

<a href="https://github.com/vitalik/django-ninja-benchmarks" target="_blank">Бенчмарки</a>:

![Django Ninja REST Framework](img/benchmark.png)

## Установка

```
pip install django-ninja
```

## Быстрый пример

Создайте новый Django-проект (или используйте существующий)
```
django-admin startproject apidemo
```

В `urls.py`

```python hl_lines="3 5 8 9 10 15"
{!./src/index001.py!}
```

Теперь запустите его как обычно:
```
./manage.py runserver
```

Примечание: вам не нужно добавлять Django Ninja в установленные приложения, чтобы он работал.

## Проверьте это

Откройте браузер на странице <a href="http://127.0.0.1:8000/api/add?a=1&b=2" target="_blank">http://127.0.0.1:8000/api/add?a=1&b=2</a>

Вы увидите JSON-ответ вида:
```JSON
{"result": 3}
```
Теперь вы только что создали API, которое:

 - Принимает HTTP GET-запрос на `/api/add`
 - Принимает, валидирует и преобразует типы GET-параметров `a` и `b`
 - Кодирует результат в JSON
 - Генерирует OpenAPI-схему для определённой операции

## Интерактивная документация API

Теперь перейдите на <a href="http://127.0.0.1:8000/api/docs" target="_blank">http://127.0.0.1:8000/api/docs</a>

Вы увидите автоматическую интерактивную документацию API (предоставляемую <a href="https://github.com/swagger-api/swagger-ui" target="_blank">OpenAPI / Swagger UI</a> или <a href="https://github.com/Redocly/redoc" target="_blank">Redoc</a>) :

![Swagger UI](img/index-swagger-ui.png)


## Итоги

Если коротко: вы объявляете типы параметров, тел запросов и т.д. всего **один раз**, как аргументы функции.

Вы делаете это с помощью стандартных современных типов Python.

Вам не нужно учить новый синтаксис, методы или классы конкретной библиотеки и т.п.

Просто стандартный **Python 3.6+**.

Например, для `int`:

```python
a: int
```

Или, для более сложной модели `Item`:

```python
class Item(Schema):
    foo: str
    bar: float

def operation(a: Item):
    ...
```

...с одним лишь этим объявлением вы получаете:

* Поддержку редактора, включая:
    * Автодополнение
    * Проверку типов
* Валидацию данных:
    * Автоматические и понятные сообщения об ошибках при некорректных данных
    * Валидацию даже для глубоко вложенных JSON-объектов
* <abbr title="Also known as: serialization, parsing, marshalling">Сериализацию</abbr> входящих сетевых данных и преобразование в выходные данные Python, с чтением из:
    * JSON
    * Параметров пути
    * Параметров запроса (query)
    * Cookies
    * Заголовков (Headers)
    * Форм
    * Файлов
* Автоматическую интерактивную документацию API

Этот проект был в значительной степени вдохновлён <a href="https://fastapi.tiangolo.com/" target="_blank">FastAPI</a>.

!!! note

    Ознакомьтесь с **[Учебником](tutorial/index.md)**, чтобы быстро начать.

    Экосистема вокруг Django Ninja:

    1. [django-ninja](index.md): Фреймворк на основе Django, берущий лучшее от Django и объединяющий его с мощью Pydantic — оптимальный выбор на пересечении безопасности и удобства.

    2. [django-ninja-crud](django-ninja-crud/index.md): Фреймворк, построенный на django-ninja для упрощения разработки CRUD-интерфейсов, предоставляющий декларативные viewsets для моделей и сценарные методы тестирования.

    3. [django-ninja-extra](django-ninja-extra/index.md): Инструмент, позволяющий разработчикам пропустить громоздкую документацию Django и быстро создавать мощные веб-приложения и современные API-интерфейсы с минимальным кодом.

    4. [django-ninja-jwt](django-ninja-jwt/index.md): Плагин JSON Web Token для django-ninja, реализующий аутентификацию и связанный функционал, форк популярного плагина Django Rest Framework.
