---
comments: true
---
# Exemple de CRUD (Create, Read, Update, Delete)


**CRUD** - **C**reate, **R**etrieve, **U**pdate, **D**elete sont les quatre fonctions de base du stockage persistant.

Cet exemple vous montrera comment implémenter ces fonctionnalités avec **Django Ninja**.

Supposons que vous ayez le modèle Django suivant sur lequel vous souhaitez effectuer ces opérations :


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

Créons maintenant des opérations CRUD pour Employee.

## C : Create

Pour créer un objet employee, vous devez définir un schéma d'entrée :

```python
from datetime import date
from ninja import Schema

class EmployeeIn(Schema):
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None

```

Ce schéma sera notre payload entrant :

```python hl_lines="2"
@api.post("/employees")
def create_employee(request, payload: EmployeeIn):
    employee = Employee.objects.create(**payload.dict())
    return {"id": employee.id}
```

!!! tip
    L'objet `Schema` possède une méthode `.dict()`, avec tous les attributs du schéma représentés sous forme de dictionnaire.

    Vous pouvez le passer sous forme de `**kwargs` à la méthode `create` du modèle Django (ou au `__init__` du modèle).

Voyez l'extrait ci-dessous pour gérer le téléversement de fichiers (via le form des modèles Django) :

```python hl_lines="2"
from ninja import UploadedFile, File

@api.post("/employees")
def create_employee(request, payload: EmployeeIn, cv: UploadedFile = File(...)):
    payload_dict = payload.dict()
    employee = Employee(**payload_dict)
    employee.cv.save(cv.name, cv) # will save model instance as well
    return {"id": employee.id}
```

Si vous n'avez besoin de téléverser qu'un seul fichier :

```python hl_lines="2"
from django.core.files.storage import FileSystemStorage
from ninja import UploadedFile, File

STORAGE = FileSystemStorage()

@api.post("/upload")
def create_upload(request, cv: UploadedFile = File(...)):
    filename = STORAGE.save(cv.name, cv)
    # Handle things further
```

## R : Read

### Objet unique

Maintenant, pour récupérer un objet employee, nous allons définir un schéma qui décrira à quoi ressemblera notre réponse. Ici, nous utiliserons essentiellement le même schéma que `EmployeeIn`, mais avec une propriété `id` supplémentaire :

```python hl_lines="2"
class EmployeeOut(Schema):
    id: int
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None
```

!!! note
    Définir un schéma de réponse n'est pas strictement requis, mais quand vous le faites, vous bénéficiez de la validation du résultat, de la documentation et de la conversion automatique des objets ORM en JSON.
Nous utiliserons ce schéma comme type `response` de notre vue `GET` pour récupérer un employé :


```python hl_lines="1"
@api.get("/employees/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    return employee
```
Notez que nous avons simplement renvoyé un objet ORM employee, sans le convertir en dictionnaire. Le schéma `response` validera automatiquement le résultat et le convertira en JSON :
```python hl_lines="4"
@api.get("/employees/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    return employee
```

### Obtenir une liste d'objets
Pour afficher une liste d'employés, nous pouvons réutiliser le même schéma `EmployeeOut`. Nous devons simplement définir le schéma de réponse sur une *List* de `EmployeeOut`.
```python hl_lines="3"
from typing import List

@api.get("/employees", response=List[EmployeeOut])
def list_employees(request):
    qs = Employee.objects.all()
    return qs
```

Une autre astuce sympathique — notez que nous venons de renvoyer un queryset de l'ORM Django :

```python hl_lines="4"
@api.get("/employees", response=List[EmployeeOut])
def list_employees(request):
    qs = Employee.objects.all()
    return qs
```
Il sera automatiquement évalué, validé et converti en liste JSON !



## U : Update

La mise à jour est assez simple. Nous utilisons simplement la méthode `PUT` et passons le `employee_id` en même temps :

```python hl_lines="1"
@api.put("/employees/{employee_id}")
def update_employee(request, employee_id: int, payload: EmployeeIn):
    employee = get_object_or_404(Employee, id=employee_id)
    for attr, value in payload.dict().items():
        setattr(employee, attr, value)
    employee.save()
    return {"success": True}
```

**Remarque**

Ici, nous avons utilisé la méthode `payload.dict` pour définir tous les attributs de l'objet :

`for attr, value in payload.dict().items()`

Vous pouvez aussi l'écrire explicitement comme ceci :

```python
employee.first_name = payload.first_name
employee.last_name = payload.last_name
employee.department_id = payload.department_id
employee.birthdate = payload.birthdate
```

**Mises à jour partielles**

Pour permettre aux utilisateurs d'effectuer des mises à jour partielles, utilisez `payload.dict(exclude_unset=True).items()`. Cela garantit que seuls les champs spécifiés seront mis à jour.

**Validation stricte des champs**

Par défaut, tout champ fourni qui n'existe pas dans le schéma est silencieusement ignoré. Pour lever une erreur pour ces champs invalides, vous pouvez définir `extra = "forbid"` dans la classe Config du schéma. Par exemple :

```python hl_lines="4 5"
class EmployeeIn(Schema):
    # your fields here...

    class Config:
        extra = "forbid"
```

## D : Delete

La suppression est également assez simple. Nous récupérons simplement l'employé par son `id` et le retirons de la base de données :


```python hl_lines="1 2 4"
@api.delete("/employees/{employee_id}")
def delete_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    return {"success": True}
```

## Code final

Voici l'exemple CRUD complet :


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

    C'est la fin du tutoriel ! Consultez les **[Guides how-to](../../guides/input/operations.md)** pour plus d'informations.

    L'écosystème autour de Django Ninja :

    1. [django-ninja-crud](../../django-ninja-crud/index.md) : un framework construit sur django-ninja pour simplifier le développement d'interfaces CRUD, offrant des model viewsets déclaratifs et des méthodes de test par scénarios.

    2. [django-ninja-extra](../../django-ninja-extra/index.md) : un outil qui permet aux développeurs de s'affranchir de la documentation Django verbeuse et de construire rapidement des applications web puissantes et des interfaces API modernes avec un minimum de code.

    3. [django-ninja-jwt](../../django-ninja-jwt/index.md) : un plugin JSON Web Token pour django-ninja qui implémente l'authentification et les fonctionnalités associées, forké d'un plugin populaire de Django Rest Framework.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
