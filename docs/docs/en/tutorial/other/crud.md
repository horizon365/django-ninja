---
comments: true
---
# CRUD (Create, Read, Update, Delete) example


**CRUD** - **C**reate, **R**etrieve, **U**pdate, **D**elete are the four basic functions of persistent storage.

This example will show you how to implement these features with **Django Ninja**.

Assume you have the following Django model that you want to perform these operations on:


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

Now let's create CRUD operations for Employee.

## C: Create

To create an employee object, you need to define an input schema:

```python
from datetime import date
from ninja import Schema

class EmployeeIn(Schema):
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None

```

This schema will be our incoming payload:

```python hl_lines="2"
@api.post("/employees")
def create_employee(request, payload: EmployeeIn):
    employee = Employee.objects.create(**payload.dict())
    return {"id": employee.id}
```

!!! tip
    The `Schema` object has a `.dict()` method, with all schema attributes represented as a dictionary.

    You can pass it as `**kwargs` to the Django model's `create` method (or the model's `__init__`).

See the snippet below to handle file uploads (via Django models' form):

```python hl_lines="2"
from ninja import UploadedFile, File

@api.post("/employees")
def create_employee(request, payload: EmployeeIn, cv: UploadedFile = File(...)):
    payload_dict = payload.dict()
    employee = Employee(**payload_dict)
    employee.cv.save(cv.name, cv) # will save model instance as well
    return {"id": employee.id}
```

If you only need to upload a single file:

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

### Single object

Now, to fetch an employee object, we will define a schema that will describe what our response will look like. Here, we will essentially use the same schema as `EmployeeIn`, but with an additional `id` property:

```python hl_lines="2"
class EmployeeOut(Schema):
    id: int
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None
```

!!! note
    Defining a response schema is not strictly required, but when you do, you get result validation, documentation, and automatic conversion of ORM objects to JSON.
We will use this schema as the `response` type of our `GET` view for retrieving an employee:


```python hl_lines="1"
@api.get("/employees/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    return employee
```
Note that we simply returned an employee ORM object, without converting it to a dictionary. The `response` schema will automatically validate the result and convert it to JSON:
```python hl_lines="4"
@api.get("/employees/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    return employee
```

### Getting a list of objects
To output a list of employees, we can reuse the same `EmployeeOut` schema. We just need to set the response schema to a *List* of `EmployeeOut`.
```python hl_lines="3"
from typing import List

@api.get("/employees", response=List[EmployeeOut])
def list_employees(request):
    qs = Employee.objects.all()
    return qs
```

Another cool trick — note that we just returned a Django ORM queryset:

```python hl_lines="4"
@api.get("/employees", response=List[EmployeeOut])
def list_employees(request):
    qs = Employee.objects.all()
    return qs
```
It will automatically be evaluated, validated, and converted into a JSON list!



## U: Update

Updating is quite simple. We just use the `PUT` method and pass the `employee_id` at the same time:

```python hl_lines="1"
@api.put("/employees/{employee_id}")
def update_employee(request, employee_id: int, payload: EmployeeIn):
    employee = get_object_or_404(Employee, id=employee_id)
    for attr, value in payload.dict().items():
        setattr(employee, attr, value)
    employee.save()
    return {"success": True}
```

**Note**

Here we used the `payload.dict` method to set all the object's attributes:

`for attr, value in payload.dict().items()`

You can also write it explicitly like this:

```python
employee.first_name = payload.first_name
employee.last_name = payload.last_name
employee.department_id = payload.department_id
employee.birthdate = payload.birthdate
```

**Partial updates**

To allow users to perform partial updates, use `payload.dict(exclude_unset=True).items()`. This ensures that only the specified fields will be updated.

**Enforcing strict field validation**

By default, any provided field that does not exist in the schema will be silently ignored. To raise an error for such invalid fields, you can set `extra = "forbid"` in the schema's Config class. For example:

```python hl_lines="4 5"
class EmployeeIn(Schema):
    # your fields here...

    class Config:
        extra = "forbid"
```

## D: Delete

Deleting is also quite simple. We just fetch the employee by `id` and remove it from the database:


```python hl_lines="1 2 4"
@api.delete("/employees/{employee_id}")
def delete_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    return {"success": True}
```

## Final code

Here is the complete CRUD example:


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

    This is the end of the tutorial! Check out the **[How-to guides](../../guides/input/operations.md)** for more information.

    Ecosystem around Django Ninja:

    1. [django-ninja-crud](../../django-ninja-crud/index.md): A framework built on django-ninja to simplify CRUD interface development, providing declarative model viewsets and scenario-based testing methods.

    2. [django-ninja-extra](../../django-ninja-extra/index.md): A tool that lets developers skip verbose Django documentation and quickly build powerful web applications and modern API interfaces with minimal code.

    3. [django-ninja-jwt](../../django-ninja-jwt/index.md): A JSON Web Token plugin for django-ninja that implements authentication and related features, forked from a popular Django Rest Framework plugin.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
