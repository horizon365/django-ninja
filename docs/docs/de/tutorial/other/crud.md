---
comments: true
---
# CRUD-Beispiel (Create, Read, Update, Delete)


**CRUD** - **C**reate, **R**etrieve, **U**pdate, **D**elete sind die vier Grundfunktionen der persistenten Speicherung.

Dieses Beispiel zeigt Ihnen, wie Sie diese Funktionen mit **Django Ninja** implementieren.

Angenommen, Sie haben das folgende Django-Modell, auf dem Sie diese Operationen ausführen möchten:


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

Erstellen wir nun CRUD-Operationen für Employee.

## C: Create

Um ein Employee-Objekt zu erstellen, müssen Sie ein Eingabe-Schema definieren:

```python
from datetime import date
from ninja import Schema

class EmployeeIn(Schema):
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None

```

Dieses Schema wird unsere eingehende Nutzlast (Payload) sein:

```python hl_lines="2"
@api.post("/employees")
def create_employee(request, payload: EmployeeIn):
    employee = Employee.objects.create(**payload.dict())
    return {"id": employee.id}
```

!!! tip
    Das `Schema`-Objekt hat eine Methode `.dict()`, bei der alle Schema-Attribute als Dictionary dargestellt werden.

    Sie können es als `**kwargs` an die Methode `create` des Django-Modells (oder an `__init__` des Modells) übergeben.

Sehen Sie sich den folgenden Ausschnitt an, um Datei-Uploads zu verarbeiten (über das Formular der Django-Modelle):

```python hl_lines="2"
from ninja import UploadedFile, File

@api.post("/employees")
def create_employee(request, payload: EmployeeIn, cv: UploadedFile = File(...)):
    payload_dict = payload.dict()
    employee = Employee(**payload_dict)
    employee.cv.save(cv.name, cv) # will save model instance as well
    return {"id": employee.id}
```

Wenn Sie nur eine einzelne Datei hochladen müssen:

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

### Einzelnes Objekt

Um nun ein Employee-Objekt abzurufen, definieren wir ein Schema, das beschreibt, wie unsere Response aussehen wird. Hier verwenden wir im Wesentlichen dasselbe Schema wie `EmployeeIn`, jedoch mit einer zusätzlichen Eigenschaft `id`:

```python hl_lines="2"
class EmployeeOut(Schema):
    id: int
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None
```

!!! note
    Ein Response-Schema zu definieren ist nicht zwingend erforderlich, aber wenn Sie es tun, erhalten Sie Ergebnisvalidierung, Dokumentation und die automatische Konvertierung von ORM-Objekten in JSON.
Wir werden dieses Schema als `response`-Typ unserer `GET`-View zum Abrufen eines Employees verwenden:


```python hl_lines="1"
@api.get("/employees/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    return employee
```
Beachten Sie, dass wir einfach ein Employee-ORM-Objekt zurückgegeben haben, ohne es in ein Dictionary zu konvertieren. Das `response`-Schema validiert das Ergebnis automatisch und konvertiert es in JSON:
```python hl_lines="4"
@api.get("/employees/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    return employee
```

### Eine Liste von Objekten abrufen
Um eine Liste von Employees auszugeben, können wir dasselbe `EmployeeOut`-Schema wiederverwenden. Wir müssen nur das Response-Schema auf eine *List* von `EmployeeOut` setzen.
```python hl_lines="3"
from typing import List

@api.get("/employees", response=List[EmployeeOut])
def list_employees(request):
    qs = Employee.objects.all()
    return qs
```

Ein weiterer cooler Trick — beachten Sie, dass wir einfach ein Django-ORM-Queryset zurückgegeben haben:

```python hl_lines="4"
@api.get("/employees", response=List[EmployeeOut])
def list_employees(request):
    qs = Employee.objects.all()
    return qs
```
Es wird automatisch ausgewertet, validiert und in eine JSON-Liste konvertiert!



## U: Update

Aktualisieren ist ziemlich einfach. Wir verwenden einfach die Methode `PUT` und übergeben gleichzeitig die `employee_id`:

```python hl_lines="1"
@api.put("/employees/{employee_id}")
def update_employee(request, employee_id: int, payload: EmployeeIn):
    employee = get_object_or_404(Employee, id=employee_id)
    for attr, value in payload.dict().items():
        setattr(employee, attr, value)
    employee.save()
    return {"success": True}
```

**Hinweis**

Hier haben wir die Methode `payload.dict` verwendet, um alle Attribute des Objekts zu setzen:

`for attr, value in payload.dict().items()`

Sie können es auch explizit so schreiben:

```python
employee.first_name = payload.first_name
employee.last_name = payload.last_name
employee.department_id = payload.department_id
employee.birthdate = payload.birthdate
```

**Partielle Updates**

Um Benutzern partielle Updates zu ermöglichen, verwenden Sie `payload.dict(exclude_unset=True).items()`. Dadurch wird sichergestellt, dass nur die angegebenen Felder aktualisiert werden.

**Strikte Feldvalidierung erzwingen**

Standardmäßig wird jedes angegebene Feld, das im Schema nicht existiert, stillschweigend ignoriert. Um bei solchen ungültigen Feldern einen Fehler auszulösen, können Sie in der Config-Klasse des Schemas `extra = "forbid"` setzen. Zum Beispiel:

```python hl_lines="4 5"
class EmployeeIn(Schema):
    # your fields here...

    class Config:
        extra = "forbid"
```

## D: Delete

Löschen ist ebenfalls ziemlich einfach. Wir holen den Employee einfach anhand der `id` und entfernen ihn aus der Datenbank:


```python hl_lines="1 2 4"
@api.delete("/employees/{employee_id}")
def delete_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    return {"success": True}
```

## Finaler Code

Hier ist das vollständige CRUD-Beispiel:


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

    Dies ist das Ende des Tutorials! Sehen Sie sich die **[How-to-Leitfäden](../../guides/input/operations.md)** für weitere Informationen an.

    Das Ökosystem rund um Django Ninja:

    1. [django-ninja-crud](../../django-ninja-crud/index.md): Ein auf django-ninja aufbauendes Framework zur Vereinfachung der Entwicklung von CRUD-Schnittstellen, mit deklarativen Model-Viewsets und szenariobasierten Testmethoden.

    2. [django-ninja-extra](../../django-ninja-extra/index.md): Ein Werkzeug, mit dem Entwickler umfangreiche Django-Dokumentation überspringen und mit minimalem Code schnell leistungsfähige Webanwendungen und moderne API-Schnittstellen erstellen können.

    3. [django-ninja-jwt](../../django-ninja-jwt/index.md): Ein JSON-Web-Token-Plugin für django-ninja, das Authentifizierung und verwandte Funktionen implementiert, geforkt von einem beliebten Django Rest Framework Plugin.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
