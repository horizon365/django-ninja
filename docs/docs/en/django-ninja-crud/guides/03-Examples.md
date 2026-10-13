---
comments: true
---
# Quick Examples
## 🌞 How It Works

Let's imagine that you are building a system for a university, and you have a model called `Department`. Each department in your university has a unique title.

```python
# examples/models.py
from django.db import models

class Department(models.Model):
    title = models.CharField(max_length=255, unique=True)
```

To interact with this data, we need a way to convert it back and forth between Python objects and a format that is easy to read and write, such as JSON. In Django Ninja, we use "Schema" to do this:

```python
# examples/schemas.py
from ninja import Schema

class DepartmentIn(Schema):
    title: str

class DepartmentOut(Schema):
    id: int
    title: str
```

The `DepartmentIn` schema defines the data we need when creating or updating a department. The `DepartmentOut` schema defines the data we will provide when retrieving a department.

Now, here comes the power of this package. With it, you can set up **CRUD** operations for the `Department` model in just a few lines of code:


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

And if your viewset is as simple as the one above, you can leverage the `APIViewSet` class to define it in a cleaner way, with default request and response bodies:
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

## ☔️ Scenario-Based Testing

Django Ninja CRUD integrates seamlessly with [Django REST Testing](https://github.com/hbakri/django-rest-testing), and ensures comprehensive coverage and robust validation of your CRUD endpoints.
Initially, the testing framework was part of this package, but it was later extracted into its own package to allow for more flexibility and to be used with other Django REST frameworks besides Django Ninja.

With this package, you can:
- **Declaratively define test scenarios**: specify the expected request and response details for each scenario, making your tests self-documenting and easy to understand.
- **Test a wide range of conditions**: validate endpoint behavior under various conditions, including valid and invalid input, non-existent resources, and custom business rules.
- **Improve clarity and maintainability**: break down tests into modular, manageable units, improving code organization and reducing technical debt.
- **Ensure comprehensive coverage**: rigorously test your endpoints thanks to the scenario-based approach, leaving no case untested.

To handle exceptions like `ObjectDoesNotExist` in your tests and return appropriate responses, you can define an exception handler like this:

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

Now, you can write tests for your CRUD views using the scenario-based testing framework:

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

By combining the declarative views of Django Ninja CRUD with the scenario-based testing capabilities of Django REST Testing, you can easily and confidently build and maintain robust, well-tested RESTful APIs.
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
