---
comments: true
---
# CRUD (Create, Read, Update, Delete) उदाहरण


**CRUD** - **C**reate, **R**etrieve, **U**pdate, **D**elete persistent storage के चार बुनियादी functions हैं।

यह उदाहरण आपको दिखाएगा कि **Django Ninja** के साथ इन features को कैसे implement करें।

मान लें कि आपके पास निम्नलिखित Django model है जिस पर आप इन operations को करना चाहते हैं:


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

अब आइए Employee के लिए CRUD operations बनाते हैं।

## C: Create

एक employee object बनाने के लिए, आपको एक input schema define करना होगा:

```python
from datetime import date
from ninja import Schema

class EmployeeIn(Schema):
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None

```

यह schema हमारा incoming payload होगा:

```python hl_lines="2"
@api.post("/employees")
def create_employee(request, payload: EmployeeIn):
    employee = Employee.objects.create(**payload.dict())
    return {"id": employee.id}
```

!!! tip
    `Schema` object की एक `.dict()` method होती है, जिसमें सभी schema attributes एक dictionary के रूप में represent होते हैं।

    आप इसे Django model के `create` method (या model के `__init__`) को `**kwargs` के रूप में pass कर सकते हैं।

File uploads (Django models के form के ज़रिए) handle करने के लिए नीचे दिया गया snippet देखें:

```python hl_lines="2"
from ninja import UploadedFile, File

@api.post("/employees")
def create_employee(request, payload: EmployeeIn, cv: UploadedFile = File(...)):
    payload_dict = payload.dict()
    employee = Employee(**payload_dict)
    employee.cv.save(cv.name, cv) # will save model instance as well
    return {"id": employee.id}
```

अगर आपको केवल एक single file upload करनी है:

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

अब, एक employee object fetch करने के लिए, हम एक schema define करेंगे जो बताएगा कि हमारा response कैसा दिखेगा। यहाँ, हम अनिवार्य रूप से वही schema इस्तेमाल करेंगे जो `EmployeeIn` है, लेकिन एक अतिरिक्त `id` property के साथ:

```python hl_lines="2"
class EmployeeOut(Schema):
    id: int
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None
```

!!! note
    Response schema define करना सख्ती से ज़रूरी नहीं है, लेकिन जब आप करते हैं, तो आपको result validation, documentation, और ORM objects का JSON में automatic conversion मिलता है।
हम इस schema को एक employee fetch करने वाले अपने `GET` view के `response` type के रूप में इस्तेमाल करेंगे:


```python hl_lines="1"
@api.get("/employees/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    return employee
```
ध्यान दें कि हमने बस एक employee ORM object return किया, उसे dictionary में convert किए बिना। `response` schema result को automatically validate करेगा और उसे JSON में convert कर देगा:
```python hl_lines="4"
@api.get("/employees/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    return employee
```

### Objects की list पाना
Employees की list output करने के लिए, हम वही `EmployeeOut` schema फिर से इस्तेमाल कर सकते हैं। हमें बस response schema को `EmployeeOut` की एक *List* पर set करना है।
```python hl_lines="3"
from typing import List

@api.get("/employees", response=List[EmployeeOut])
def list_employees(request):
    qs = Employee.objects.all()
    return qs
```

एक और शानदार trick — ध्यान दें कि हमने बस एक Django ORM queryset return किया:

```python hl_lines="4"
@api.get("/employees", response=List[EmployeeOut])
def list_employees(request):
    qs = Employee.objects.all()
    return qs
```
इसे automatically evaluate, validate, और एक JSON list में convert कर दिया जाएगा!



## U: Update

Update करना काफ़ी आसान है। हम बस `PUT` method का इस्तेमाल करते हैं और साथ में `employee_id` pass करते हैं:

```python hl_lines="1"
@api.put("/employees/{employee_id}")
def update_employee(request, employee_id: int, payload: EmployeeIn):
    employee = get_object_or_404(Employee, id=employee_id)
    for attr, value in payload.dict().items():
        setattr(employee, attr, value)
    employee.save()
    return {"success": True}
```

**ध्यान दें**

यहाँ हमने object के सभी attributes set करने के लिए `payload.dict` method का इस्तेमाल किया:

`for attr, value in payload.dict().items()`

आप इसे इस तरह स्पष्ट रूप से भी लिख सकते हैं:

```python
employee.first_name = payload.first_name
employee.last_name = payload.last_name
employee.department_id = payload.department_id
employee.birthdate = payload.birthdate
```

**Partial updates**

Users को partial updates करने देने के लिए, `payload.dict(exclude_unset=True).items()` का इस्तेमाल करें। इससे यह सुनिश्चित होता है कि केवल specified fields ही update होंगे।

**Strict field validation लागू करना**

डिफ़ॉल्ट रूप से, schema में मौजूद न होने वाले किसी भी दिए गए field को silently ignore कर दिया जाता है। ऐसे invalid fields के लिए error raise करने के लिए, आप schema की Config class में `extra = "forbid"` set कर सकते हैं। उदाहरण के लिए:

```python hl_lines="4 5"
class EmployeeIn(Schema):
    # your fields here...

    class Config:
        extra = "forbid"
```

## D: Delete

Delete करना भी काफ़ी आसान है। हम बस `id` से employee को fetch करते हैं और database से हटा देते हैं:


```python hl_lines="1 2 4"
@api.delete("/employees/{employee_id}")
def delete_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    return {"success": True}
```

## Final code

यहाँ पूरा CRUD उदाहरण है:


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

    Tutorial यहीं समाप्त होता है! अधिक जानकारी के लिए **[How-to guides](../../guides/input/operations.md)** देखें।

    Django Ninja के आस-पास का ecosystem:

    1. [django-ninja-crud](../../django-ninja-crud/index.md): django-ninja पर बना एक framework जो CRUD interface development को आसान बनाता है, जो declarative model viewsets और scenario-आधारित testing methods प्रदान करता है।

    2. [django-ninja-extra](../../django-ninja-extra/index.md): एक tool जो developers को लंबे-चौड़े Django documentation से बचाता है और न्यूनतम code के साथ तेज़ी से शक्तिशाली web applications और आधुनिक API interfaces बनाने देता है।

    3. [django-ninja-jwt](../../django-ninja-jwt/index.md): django-ninja के लिए एक JSON Web Token plugin जो authentication और संबंधित features implement करता है, जो एक लोकप्रिय Django Rest Framework plugin से fork किया गया है।

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
