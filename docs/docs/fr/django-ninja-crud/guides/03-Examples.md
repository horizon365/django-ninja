---
comments: true
---
# Exemples rapides
## 🌞 Comment ça fonctionne

Imaginons que vous construisez un système pour une université, et que vous disposiez d'un modèle appelé `Department`. Chaque département de votre université possède un titre unique.

```python
# examples/models.py
from django.db import models

class Department(models.Model):
    title = models.CharField(max_length=255, unique=True)
```

Pour interagir avec ces données, nous avons besoin d'un moyen de les convertir dans les deux sens entre des objets Python et un format facile à lire et à écrire, comme JSON. Dans Django Ninja, nous utilisons des « Schema » pour cela :

```python
# examples/schemas.py
from ninja import Schema

class DepartmentIn(Schema):
    title: str

class DepartmentOut(Schema):
    id: int
    title: str
```

Le schéma `DepartmentIn` définit les données dont nous avons besoin lors de la création ou de la mise à jour d'un département. Le schéma `DepartmentOut` définit les données que nous fournirons lors de la récupération d'un département.

Maintenant, voici la puissance de ce paquet. Avec lui, vous pouvez mettre en place des opérations **CRUD** pour le modèle `Department` en seulement quelques lignes de code :


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

Et si votre viewset est aussi simple que celui ci-dessus, vous pouvez utiliser la classe `APIViewSet` pour le définir de manière plus propre, avec des corps de requête et de réponse par défaut :
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

## ☔️ Tests basés sur des scénarios

Django Ninja CRUD s'intègre parfaitement avec [Django REST Testing](https://github.com/hbakri/django-rest-testing) et garantit une couverture complète et une validation robuste de vos endpoints CRUD.
Initialement, le framework de test faisait partie de ce paquet, mais il a ensuite été extrait dans son propre paquet pour permettre plus de flexibilité et pour être utilisé avec d'autres frameworks Django REST outre Django Ninja.

Avec ce paquet, vous pouvez :
- **Définir déclarativement des scénarios de test** : spécifiez les détails attendus de la requête et de la réponse pour chaque scénario, rendant vos tests auto-documentés et faciles à comprendre.
- **Tester une large gamme de conditions** : validez le comportement des endpoints dans diverses conditions, y compris les entrées valides et invalides, les ressources inexistantes et les règles métier personnalisées.
- **Améliorer la clarté et la maintenabilité** : décomposez les tests en unités modulaires et gérables, améliorant l'organisation du code et réduisant la dette technique.
- **Garantir une couverture complète** : testez rigoureusement vos endpoints grâce à l'approche basée sur des scénarios, ne laissant aucun cas non testé.

Pour gérer les exceptions comme `ObjectDoesNotExist` dans vos tests et renvoyer des réponses appropriées, vous pouvez définir un gestionnaire d'exceptions comme ceci :

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

Maintenant, vous pouvez écrire des tests pour vos vues CRUD en utilisant le framework de test basé sur des scénarios :

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

En combinant les vues déclaratives de Django Ninja CRUD avec les capacités de test basées sur des scénarios de Django REST Testing, vous pouvez facilement et en toute confiance construire et maintenir des API RESTful robustes et bien testées.
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
