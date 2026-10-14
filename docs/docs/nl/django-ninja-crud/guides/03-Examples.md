---
comments: true
---
# Snelle voorbeelden
## 🌞 Hoe het werkt

Stel je voor dat je een systeem voor een universiteit bouwt en je een model hebt dat `Department` heet. Elke afdeling aan je universiteit heeft een unieke titel.

```python
# examples/models.py
from django.db import models

class Department(models.Model):
    title = models.CharField(max_length=255, unique=True)
```

Om met deze gegevens te werken, hebben we een manier nodig om ze heen en weer te converteren tussen Python-objecten en een formaat dat makkelijk te lezen en schrijven is, zoals JSON. In Django Ninja gebruiken we daarvoor een "Schema":

```python
# examples/schemas.py
from ninja import Schema

class DepartmentIn(Schema):
    title: str

class DepartmentOut(Schema):
    id: int
    title: str
```

Het schema `DepartmentIn` definieert de gegevens die we nodig hebben bij het aanmaken of bijwerken van een afdeling. Het schema `DepartmentOut` definieert de gegevens die we verstrekken bij het ophalen van een afdeling.

En nu komt de kracht van dit pakket. ermee kun je in slechts een paar regels code **CRUD**-bewerkingen voor het model `Department` opzetten:


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

En als je viewset net zo eenvoudig is als die hierboven, kun je de klasse `APIViewSet` gebruiken om deze op een schonere manier te definiëren, met standaard request- en response-bodies:
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

## ☔️ Testen op basis van scenario's

Django Ninja CRUD integreert naadloos met [Django REST Testing](https://github.com/hbakri/django-rest-testing) en zorgt voor uitgebreide dekking en robuuste validatie van je CRUD-endpoints.
Aanvankelijk maakte het testframework deel uit van dit pakket, maar het werd later afgesplitst in een eigen pakket voor meer flexibiliteit en om het ook samen met andere Django REST-frameworks naast Django Ninja te kunnen gebruiken.

Met dit pakket kun je:
- **Declaratief testschema's definiëren**: geef de verwachte details van request en response voor elk scenario op, waardoor je tests zichzelf documenteren en gemakkelijk te begrijpen zijn.
- **Een breed scala aan omstandigheden testen**: valideer het gedrag van endpoints onder verschillende omstandigheden, waaronder geldige en ongeldige invoer, niet-bestaande resources en aangepaste bedrijfsregels.
- **Duidelijkheid en onderhoudbaarheid verbeteren**: splits tests op in modulaire, beheersbare eenheden, wat de codeorganisatie verbetert en technische schulden vermindert.
- **Uitgebreide dekking waarborgen**: test je endpoints rigoureus dankzij de op scenario's gebaseerde aanpak, zodat geen enkel geval ongetest blijft.

Om uitzonderingen zoals `ObjectDoesNotExist` in je tests af te handelen en passende responses terug te geven, kun je een exception-handler als volgt definiëren:

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

Nu kun je tests schrijven voor je CRUD-views met het op scenario's gebaseerde testframework:

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

Door de declaratieve views van Django Ninja CRUD te combineren met de op scenario's gebaseerde testmogelijkheden van Django REST Testing, kun je gemakkelijk en vol vertrouwen robuuste, goed geteste RESTful API's bouwen en onderhouden.
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
