---
comments: true
---
# CRUD (Create, Read, Update, Delete) voorbeeld


**CRUD** - **C**reate, **R**etrieve, **U**pdate, **D**elete zijn de vier basisfuncties van persistente opslag.

Dit voorbeeld laat je zien hoe je deze functies implementeert met **Django Ninja**.

Stel dat je het volgende Django-model hebt waarop je deze operaties wilt uitvoeren:


```python

class Department(models.Model):
    title = models.CharField(max_length=100)

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    birthdate = models.DateField(null=True, blank=True)
    cv = models.FileField(null=True, blank=True)
```

Laten we nu CRUD-operaties maken voor Employee.

## C: Create

Om een employee-object aan te maken, moet je een input-schema definiëren:

```python
from datetime import date
from ninja import Schema

class EmployeeIn(Schema):
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None

```

Dit schema zal onze inkomende payload zijn:

```python hl_lines="2"
@api.post("/employees")
def create_employee(request, payload: EmployeeIn):
    employee = Employee.objects.create(**payload.dict())
    return {"id": employee.id}
```

!!! tip
    Het `Schema`-object heeft een `.dict()`-methode, waarbij alle schema-attributen worden weergegeven als een dictionary.

    Je kunt dit als `**kwargs` doorgeven aan de `create`-methode van het Django-model (of de `__init__` van het model).

Zie het onderstaande fragment voor het verwerken van bestandsuploads (via de formulieren van Django-modellen):

```python hl_lines="2"
from ninja import UploadedFile, File

@api.post("/employees")
def create_employee(request, payload: EmployeeIn, cv: UploadedFile = File(...)):
    payload_dict = payload.dict()
    employee = Employee(**payload_dict)
    employee.cv.save(cv.name, cv) # will save model instance as well
    return {"id": employee.id}
```

Als je slechts één enkel bestand hoeft te uploaden:

```python hl_lines="2"
from django.core.files.storage import FileSystemStorage
from ninja import UploadedFile, File

STORAGE = FileSystemStorage()

@api.post("/upload")
def create_upload(request, cv: UploadedFile = File(...)):
    filename = STORAGE.save(cv.name, cv)
    # Handle things further
```

## R: Read

### Enkel object

Laten we nu, om een employee-object op te halen, een schema definiëren dat beschrijft hoe onze response eruit zal zien. Hier zullen we in wezen hetzelfde schema gebruiken als `EmployeeIn`, maar met een extra eigenschap `id`:

```python hl_lines="2"
class EmployeeOut(Schema):
    id: int
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None
```

!!! note
    Het definiëren van een response-schema is niet strikt noodzakelijk, maar als je dit doet, krijg je resultaatvalidatie, documentatie en automatische conversie van ORM-objecten naar JSON.
We zullen dit schema gebruiken als het `response`-type van onze `GET`-view voor het ophalen van een employee:


```python hl_lines="1"
@api.get("/employees/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    return employee
```
Merk op dat we simpelweg een employee-ORM-object retourneerden, zonder het naar een dictionary te converteren. Het `response`-schema zal het resultaat automatisch valideren en naar JSON converteren:
```python hl_lines="4"
@api.get("/employees/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    return employee
```

### Een lijst met objecten ophalen
Om een lijst met employees als uitvoer te geven, kunnen we hetzelfde `EmployeeOut`-schema hergebruiken. We hoeven het response-schema alleen in te stellen op een *List* van `EmployeeOut`.
```python hl_lines="3"
from typing import List

@api.get("/employees", response=List[EmployeeOut])
def list_employees(request):
    qs = Employee.objects.all()
    return qs
```

Nog een handige truc — merk op dat we gewoon een Django ORM queryset retourneerden:

```python hl_lines="4"
@api.get("/employees", response=List[EmployeeOut])
def list_employees(request):
    qs = Employee.objects.all()
    return qs
```
Deze wordt automatisch geëvalueerd, gevalideerd en omgezet in een JSON-lijst!



## U: Update

Bijwerken is vrij eenvoudig. We gebruiken gewoon de `PUT`-methode en geven tegelijk de `employee_id` door:

```python hl_lines="1"
@api.put("/employees/{employee_id}")
def update_employee(request, employee_id: int, payload: EmployeeIn):
    employee = get_object_or_404(Employee, id=employee_id)
    for attr, value in payload.dict().items():
        setattr(employee, attr, value)
    employee.save()
    return {"success": True}
```

**Let op**

Hier gebruikten we de methode `payload.dict` om alle attributen van het object in te stellen:

`for attr, value in payload.dict().items()`

Je kunt het ook expliciet zo opschrijven:

```python
employee.first_name = payload.first_name
employee.last_name = payload.last_name
employee.department_id = payload.department_id
employee.birthdate = payload.birthdate
```

**Gedeeltelijke updates**

Om gebruikers gedeeltelijke updates te laten uitvoeren, gebruik je `payload.dict(exclude_unset=True).items()`. Dit zorgt ervoor dat alleen de opgegeven velden worden bijgewerkt.

**Strikte veldvalidatie afdwingen**

Standaard wordt elk opgegeven veld dat niet in het schema bestaat, stilletjes genegeerd. Om een foutmelding te geven voor zulke ongeldige velden, kun je `extra = "forbid"` instellen in de Config-klasse van het schema. Bijvoorbeeld:

```python hl_lines="4 5"
class EmployeeIn(Schema):
    # your fields here...

    class Config:
        extra = "forbid"
```

## D: Delete

Verwijderen is ook vrij eenvoudig. We halen de employee gewoon op basis van `id` op en verwijderen deze uit de database:


```python hl_lines="1 2 4"
@api.delete("/employees/{employee_id}")
def delete_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    return {"success": True}
```

## Volledige code

Hier is het complete CRUD-voorbeeld:


```python
from datetime import date
from typing import List
from ninja import NinjaAPI, Schema
from django.shortcuts import get_object_or_404
from employees.models import Employee


api = NinjaAPI()


class EmployeeIn(Schema):
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None


class EmployeeOut(Schema):
    id: int
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None


@api.post("/employees")
def create_employee(request, payload: EmployeeIn):
    employee = Employee.objects.create(**payload.dict())
    return {"id": employee.id}


@api.get("/employees/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    return employee


@api.get("/employees", response=List[EmployeeOut])
def list_employees(request):
    qs = Employee.objects.all()
    return qs


@api.put("/employees/{employee_id}")
def update_employee(request, employee_id: int, payload: EmployeeIn):
    employee = get_object_or_404(Employee, id=employee_id)
    for attr, value in payload.dict().items():
        setattr(employee, attr, value)
    employee.save()
    return {"success": True}


@api.delete("/employees/{employee_id}")
def delete_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    return {"success": True}
```

!!! success

    Dit is het einde van de tutorial! Bekijk de **[How-to guides](../../guides/input/operations.md)** voor meer informatie.

    Het ecosysteem rond Django Ninja:

    1. [django-ninja-crud](../../django-ninja-crud/index.md): Een framework gebouwd op django-ninja om de ontwikkeling van CRUD-interfaces te vereenvoudigen, met declaratieve model-viewsets en scenario-gebaseerde testmethoden.

    2. [django-ninja-extra](../../django-ninja-extra/index.md): Een tool waarmee ontwikkelaars de uitgebreide Django-documentatie kunnen overslaan en met minimale code snel krachtige webapplicaties en moderne API-interfaces kunnen bouwen.

    3. [django-ninja-jwt](../../django-ninja-jwt/index.md): Een JSON Web Token-plugin voor django-ninja die authenticatie en verwante functies implementeert, geforkt van een populaire Django Rest Framework-plugin.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
