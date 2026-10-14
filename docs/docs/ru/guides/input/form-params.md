---
comments: true
---
# Данные формы

**Django Ninja** также позволяет разбирать и проверять данные `request.POST`
(то есть `application/x-www-form-urlencoded` или `multipart/form-data`).

## Данные формы как параметры

```python hl_lines="1 4"
from ninja import NinjaAPI, Form

@api.post("/login")
def login(request, username: Form[str], password: Form[str]):
    return {'username': username, 'password': '*****'}
```

Обратите внимание на следующее:

1) Нужно импортировать класс `Form` из `ninja`
```python
from ninja import Form
```

2) Используйте `Form` в качестве значения параметра по умолчанию:
```python
username: Form[str]
```

## Использование схемы

Как и в случае с [телом запроса](body.md#declare-it-as-a-parameter), вы можете использовать схему для организации ваших параметров.

```python hl_lines="12"
{!./src/tutorial/form/code01.py!}
```

## Форма запроса + параметры пути + параметры запроса

Как и в случае с [телом запроса](body.md#request-body-path-query-parameters), вы можете комбинировать данные формы с другими источниками параметров.

Вы можете одновременно объявлять параметры запроса **и** параметры пути **и** поля формы **и т. д.**

**Django Ninja** распознает, что параметры функции, совпадающие с параметрами пути, должны **браться из пути**,
параметры функции, объявленные с `Form(...)`, должны **браться из полей формы запроса**, и так далее.

```python hl_lines="12"
{!./src/tutorial/form/code02.py!}
```
## Сопоставление пустых полей формы со значениями по умолчанию

Необязательные поля формы часто отправляются с пустыми значениями. Это значение интерпретируется как пустая строка, поэтому для полей типа `int` или `bool` проверка может завершиться ошибкой.

Как описано в документации Pydantic, это можно решить, используя [обобщённые классы в качестве типов](https://pydantic.com.cn/usage/types/#generic-classes-as-types).

```python hl_lines="15 16 23-25"
{!./src/tutorial/form/code03.py!}
```

!!! done

    Переходите к следующей главе! **[Загрузка файлов](file-params.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
