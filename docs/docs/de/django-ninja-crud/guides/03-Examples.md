---
comments: true
---
# Kurze Beispiele
## 🌞 Wie es funktioniert

Stellen wir uns vor, dass Sie ein System für eine Universität bauen und ein Modell namens `Department` haben. Jede Fakultät (Department) Ihrer Universität hat einen eindeutigen Titel.

```python
# examples/models.py
from django.db import models

class Department(models.Model):
    title = models.CharField(max_length=255, unique=True)
```

Um mit diesen Daten zu interagieren, benötigen wir eine Möglichkeit, sie zwischen Python-Objekten und einem Format, das sich leicht lesen und schreiben lässt, wie etwa JSON, hin und her zu konvertieren. In Django Ninja verwenden wir dafür ein „Schema":

```python
# examples/schemas.py
from ninja import Schema

class DepartmentIn(Schema):
    title: str

class DepartmentOut(Schema):
    id: int
    title: str
```

Das `DepartmentIn`-Schema definiert die Daten, die wir beim Erstellen oder Aktualisieren einer Fakultät benötigen. Das `DepartmentOut`-Schema definiert die Daten, die wir beim Abrufen einer Fakultät bereitstellen werden.

Nun kommt die Stärke dieses Pakets ins Spiel. Damit können Sie **CRUD**-Operationen für das Modell `Department` mit nur wenigen Codezeilen einrichten:


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

Und wenn Ihr ViewSet so einfach ist wie das obige, können Sie die Klasse `APIViewSet` nutzen, um es auf eine übersichtlichere Weise mit Standard-Request- und Response-Bodies zu definieren:
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

## ☔️ Szenariobasiertes Testen

Django Ninja CRUD integriert sich nahtlos mit [Django REST Testing](https://github.com/hbakri/django-rest-testing) und stellt eine umfassende Abdeckung sowie eine robuste Validierung Ihrer CRUD-Endpunkte sicher.
Anfangs war das Testframework Teil dieses Pakets, wurde später jedoch in ein eigenes Paket ausgelagert, um mehr Flexibilität zu ermöglichen und es neben Django Ninja auch mit anderen Django-REST-Frameworks verwenden zu können.

Mit diesem Paket können Sie:
- **Testfälle deklarativ definieren**: geben Sie die erwarteten Request- und Response-Details für jedes Szenario an, wodurch Ihre Tests selbstdokumentierend und leicht verständlich werden.
- **Ein breites Spektrum an Bedingungen testen**: validieren Sie das Endpunktverhalten unter verschiedenen Bedingungen, einschließlich gültiger und ungültiger Eingaben, nicht existierender Ressourcen und benutzerdefinierter Geschäftsregeln.
- **Klarheit und Wartbarkeit verbessern**: gliedern Sie Tests in modulare, überschaubare Einheiten, verbessern Sie die Codeorganisation und reduzieren Sie technische Schulden.
- **Umfassende Abdeckung sicherstellen**: testen Sie Ihre Endpunkte dank des szenariobasierten Ansatzes gründlich, sodass kein Fall ungetestet bleibt.

Um in Ihren Tests Ausnahmen wie `ObjectDoesNotExist` zu behandeln und entsprechende Antworten zurückzugeben, können Sie einen Exception-Handler wie folgt definieren:

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

Nun können Sie mit dem szenariobasierten Testframework Tests für Ihre CRUD-Views schreiben:

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

Durch die Kombination der deklarativen Views von Django Ninja CRUD mit den szenariobasierten Testmöglichkeiten von Django REST Testing können Sie robuste, gut getestete RESTful-APIs mühelos und mit Zuversicht aufbauen und pflegen.
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
