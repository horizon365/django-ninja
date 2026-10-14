---
comments: true
---
# Быстрые примеры
## 🌞 Как это работает

Давайте представим, что вы создаёте систему для университета, и у вас есть модель под названием `Department`. Каждый факультет в вашем университете имеет уникальное название.

```python
# examples/models.py
from django.db import models

class Department(models.Model):
    title = models.CharField(max_length=255, unique=True)
```

Для взаимодействия с этими данными нам нужен способ преобразовывать их туда и обратно между объектами Python и форматом, который легко читать и записывать, например JSON. В Django Ninja для этого мы используем «Schema»:

```python
# examples/schemas.py
from ninja import Schema

class DepartmentIn(Schema):
    title: str

class DepartmentOut(Schema):
    id: int
    title: str
```

Схема `DepartmentIn` определяет данные, которые нам нужны при создании или обновлении факультета. Схема `DepartmentOut` определяет данные, которые мы будем предоставлять при получении факультета.

А теперь наступает сила этого пакета. С его помощью вы можете настроить **CRUD**-операции для модели `Department` всего в нескольких строках кода:


```python
# examples/views/department_views.py
from typing import List
from django.http import HttpRequest
from ninja import NinjaAPI
from ninja_crud import views, viewsets

from examples.models import Department
from examples.schemas import DepartmentIn, DepartmentOut

api = NinjaAPI()


class DepartmentViewSet(viewsets.APIViewSet):
    api = api
    model = Department

    list_departments = views.ListView(
        response_body=List[DepartmentOut]
    )
    create_department = views.CreateView(
        request_body=DepartmentIn,
        response_body=DepartmentOut,
    )
    read_department = views.ReadView(
        response_body=DepartmentOut
    )
    update_department = views.UpdateView(
        request_body=DepartmentIn,
        response_body=DepartmentOut,
    )
    delete_department = views.DeleteView()


# In addition to the CRUD operations managed by the viewset,
# the api or router can be used in the standard Django Ninja way
@api.get("/statistics/", response=dict)
def get_department_statistics(request: HttpRequest):
    return {"total": Department.objects.count()}
```

А если ваш viewset настолько же прост, как приведённый выше, вы можете воспользоваться классом `APIViewSet`, чтобы определить его более аккуратно, с телами запросов и ответов по умолчанию:
```python
# examples/views/department_views.py
from ninja import NinjaAPI
from ninja_crud import views, viewsets

from examples.models import Department
from examples.schemas import DepartmentIn, DepartmentOut

api = NinjaAPI()


class DepartmentViewSet(viewsets.APIViewSet):
    api = api
    model = Department
    default_request_body = DepartmentIn
    default_response_body = DepartmentOut

    list_departments = views.ListView()
    create_department = views.CreateView()
    read_department = views.ReadView()
    update_department = views.UpdateView()
    delete_department = views.DeleteView()
```

## ☔️ Сценарное тестирование

Django Ninja CRUD бесшовно интегрируется с [Django REST Testing](https://github.com/hbakri/django-rest-testing) и обеспечивает всесторонний охват и надёжную валидацию ваших CRUD-эндпоинтов.
Изначально фреймворк тестирования был частью этого пакета, но позже он был выделен в отдельный пакет, чтобы обеспечить большую гибкость и возможность использования с другими Django REST-фреймворками помимо Django Ninja.

С этим пакетом вы можете:
- **Декларативно определять тестовые сценарии**: указывать ожидаемые детали запроса и ответа для каждого сценария, делая ваши тесты самодокументируемыми и лёгкими для понимания.
- **Тестировать широкий спектр условий**: проверять поведение эндпоинта в различных условиях, включая корректный и некорректный ввод, несуществующие ресурсы и кастомные бизнес-правила.
- **Повышать ясность и сопровождаемость**: разбивать тесты на модульные, управляемые единицы, улучшая организацию кода и снижая технический долг.
- **Обеспечивать всесторонний охват**: тщательно тестировать ваши эндпоинты благодаря сценарному подходу, не оставляя непроверенных случаев.

Чтобы обрабатывать исключения вроде `ObjectDoesNotExist` в ваших тестах и возвращать соответствующие ответы, вы можете определить обработчик исключений следующим образом:

```python
# examples/exception_handlers.py
from ninja import NinjaAPI
from django.core.exceptions import ObjectDoesNotExist

api = NinjaAPI()


@api.exception_handler(ObjectDoesNotExist)
def handle_object_does_not_exist(request, exc):
    return api.create_response(
        request,
        {"message": "ObjectDoesNotExist", "detail": str(exc)},
        status=404,
    )

# ... other exception handlers
```

Теперь вы можете писать тесты для ваших CRUD-views, используя сценарный фреймворк тестирования:

```python
# examples/tests/test_department_views.py
from examples.models import Department
from examples.schemas import DepartmentOut

from ninja_crud.testing import APITestCase, APIViewTestScenario


class TestDepartmentViewSet(APITestCase):
    department: Department

    @classmethod
    def setUpTestData(cls):
        cls.department = Department.objects.create(title="department")

    def test_read_department(self):
        self.assertScenariosSucceed(
            method="GET",
            path="/api/departments/{id}",
            scenarios=[
                APIViewTestScenario(
                    path_parameters={"id": self.department.id},
                    expected_response_status=200,
                    expected_response_body_type=DepartmentOut,
                    expected_response_body={
                        "id": self.department.id,
                        "title": self.department.title,
                    },
                ),
                APIViewTestScenario(
                    path_parameters={"id": 9999},
                    expected_response_status=404,
                ),
            ],
        )
```

Комбинируя декларативные views Django Ninja CRUD со сценарными возможностями тестирования Django REST Testing, вы можете легко и уверенно создавать и сопровождать надёжные, хорошо протестированные RESTful API.
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
