---
comments: true
---
# Пример CRUD (Create, Read, Update, Delete)


**CRUD** — **C**reate, **R**etrieve, **U**pdate, **D**elete — это четыре базовые функции постоянного хранилища.

Этот пример покажет вам, как реализовать эти возможности с помощью **Django Ninja**.

Предположим, у вас есть следующая Django-модель, над которой вы хотите выполнять эти операции:


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

Теперь давайте создадим CRUD-операции для Employee.

## C: Create (Создание)

Чтобы создать объект employee, нужно определить входную схему:

```python
from datetime import date
from ninja import Schema

class EmployeeIn(Schema):
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None

```

Эта схема будет нашим входящим payload:

```python hl_lines="2"
@api.post("/employees")
def create_employee(request, payload: EmployeeIn):
    employee = Employee.objects.create(**payload.dict())
    return {"id": employee.id}
```

!!! tip
    У объекта `Schema` есть метод `.dict()`, который возвращает все атрибуты схемы в виде словаря.

    Его можно передать как `**kwargs` в метод `create` Django-модели (или в `__init__` модели).

См. фрагмент ниже для обработки загрузки файлов (через формы Django-моделей):

```python hl_lines="2"
from ninja import UploadedFile, File

@api.post("/employees")
def create_employee(request, payload: EmployeeIn, cv: UploadedFile = File(...)):
    payload_dict = payload.dict()
    employee = Employee(**payload_dict)
    employee.cv.save(cv.name, cv) # will save model instance as well
    return {"id": employee.id}
```

Если вам нужно загрузить только один файл:

```python hl_lines="2"
from django.core.files.storage import FileSystemStorage
from ninja import UploadedFile, File

STORAGE = FileSystemStorage()

@api.post("/upload")
def create_upload(request, cv: UploadedFile = File(...)):
    filename = STORAGE.save(cv.name, cv)
    # Handle things further
```

## R: Read (Чтение)

### Один объект

Теперь, чтобы получить объект employee, мы определим схему, которая описывает, как будет выглядеть наш ответ. Здесь мы, по сути, будем использовать ту же схему, что и `EmployeeIn`, но с дополнительным свойством `id`:

```python hl_lines="2"
class EmployeeOut(Schema):
    id: int
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None
```

!!! note
    Определение схемы ответа не является строго обязательным, но когда вы это делаете, вы получаете валидацию результата, документацию и автоматическое преобразование ORM-объектов в JSON.
Мы будем использовать эту схему как тип `response` нашего `GET`-представления для получения employee:


```python hl_lines="1"
@api.get("/employees/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    return employee
```
Обратите внимание, что мы просто вернули ORM-объект employee, не преобразуя его в словарь. Схема `response` автоматически провалидирует результат и преобразует его в JSON:
```python hl_lines="4"
@api.get("/employees/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    return employee
```

### Получение списка объектов
Чтобы вывести список employees, мы можем переиспользовать ту же схему `EmployeeOut`. Нам просто нужно установить схему ответа в *List* из `EmployeeOut`.
```python hl_lines="3"
from typing import List

@api.get("/employees", response=List[EmployeeOut])
def list_employees(request):
    qs = Employee.objects.all()
    return qs
```

Ещё один классный приём — обратите внимание, что мы просто вернули queryset Django ORM:

```python hl_lines="4"
@api.get("/employees", response=List[EmployeeOut])
def list_employees(request):
    qs = Employee.objects.all()
    return qs
```
Он будет автоматически вычислен, провалидирован и преобразован в JSON-список!



## U: Update (Обновление)

Обновление довольно простое. Мы просто используем метод `PUT` и одновременно передаём `employee_id`:

```python hl_lines="1"
@api.put("/employees/{employee_id}")
def update_employee(request, employee_id: int, payload: EmployeeIn):
    employee = get_object_or_404(Employee, id=employee_id)
    for attr, value in payload.dict().items():
        setattr(employee, attr, value)
    employee.save()
    return {"success": True}
```

**Примечание**

Здесь мы использовали метод `payload.dict`, чтобы установить все атрибуты объекта:

`for attr, value in payload.dict().items()`

Вы также можете записать это явно вот так:

```python
employee.first_name = payload.first_name
employee.last_name = payload.last_name
employee.department_id = payload.department_id
employee.birthdate = payload.birthdate
```

**Частичные обновления**

Чтобы позволить пользователям выполнять частичные обновления, используйте `payload.dict(exclude_unset=True).items()`. Это гарантирует, что будут обновлены только указанные поля.

**Строгая валидация полей**

По умолчанию любое переданное поле, отсутствующее в схеме, молча игнорируется. Чтобы вызывать ошибку для таких некорректных полей, вы можете установить `extra = "forbid"` в классе Config схемы. Например:

```python hl_lines="4 5"
class EmployeeIn(Schema):
    # your fields here...

    class Config:
        extra = "forbid"
```

## D: Delete (Удаление)

Удаление тоже довольно простое. Мы просто находим employee по `id` и удаляем его из базы данных:


```python hl_lines="1 2 4"
@api.delete("/employees/{employee_id}")
def delete_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    return {"success": True}
```

## Итоговый код

Вот полный CRUD-пример:


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

    Это конец учебника! Ознакомьтесь с **[How-to руководствами](../../guides/input/operations.md)** для получения дополнительной информации.

    Экосистема вокруг Django Ninja:

    1. [django-ninja-crud](../../django-ninja-crud/index.md): Фреймворк, построенный на django-ninja для упрощения разработки CRUD-интерфейсов, предоставляющий декларативные viewsets для моделей и сценарные методы тестирования.

    2. [django-ninja-extra](../../django-ninja-extra/index.md): Инструмент, позволяющий разработчикам пропустить громоздкую документацию Django и быстро создавать мощные веб-приложения и современные API-интерфейсы с минимальным кодом.

    3. [django-ninja-jwt](../../django-ninja-jwt/index.md): Плагин JSON Web Token для django-ninja, реализующий аутентификацию и связанный функционал, форк популярного плагина Django Rest Framework.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
