---
comments: true
---
# CRUD (Create, Read, Update, Delete) 예제


**CRUD** - **C**reate, **R**etrieve, **U**pdate, **D**elete는 영구 저장소의 네 가지 기본 기능입니다.

이 예제에서는 **Django Ninja**로 이러한 기능을 구현하는 방법을 보여줍니다.

다음과 같이 이러한 operation을 수행하고 싶은 Django 모델이 있다고 가정합니다:


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

이제 Employee를 위한 CRUD operation을 만들어 보겠습니다.

## C: Create

employee 객체를 생성하려면 입력 schema를 정의해야 합니다:

```python
from datetime import date
from ninja import Schema

class EmployeeIn(Schema):
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None

```

이 schema가 곧 들어오는 payload가 됩니다:

```python hl_lines="2"
@api.post("/employees")
def create_employee(request, payload: EmployeeIn):
    employee = Employee.objects.create(**payload.dict())
    return {"id": employee.id}
```

!!! tip
    `Schema` 객체에는 모든 schema 속성이 dictionary로 표현되는 `.dict()` 메서드가 있습니다.

    이를 `**kwargs`로 Django 모델의 `create` 메서드(또는 모델의 `__init__`)에 전달할 수 있습니다.

파일 업로드를 처리하는 방법은 아래 스니펫을 참조하세요 (Django 모델의 form을 통해):

```python hl_lines="2"
from ninja import UploadedFile, File

@api.post("/employees")
def create_employee(request, payload: EmployeeIn, cv: UploadedFile = File(...)):
    payload_dict = payload.dict()
    employee = Employee(**payload_dict)
    employee.cv.save(cv.name, cv) # will save model instance as well
    return {"id": employee.id}
```

단일 파일만 업로드하면 되는 경우:

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

### 단일 객체

이제 employee 객체를 가져오기 위해, 응답이 어떤 모습일지 기술하는 schema를 정의하겠습니다. 여기서는 본질적으로 `EmployeeIn`과 동일한 schema를 사용하되, `id` 속성을 하나 추가합니다:

```python hl_lines="2"
class EmployeeOut(Schema):
    id: int
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None
```

!!! note
    response schema를 정의하는 것은 엄격히 필수는 아니지만, 정의하면 결과 검증, 문서화, 그리고 ORM 객체의 JSON 자동 변환의 이점을 얻을 수 있습니다.
employee를 가져오는 `GET` view의 `response` 타입으로 이 schema를 사용하겠습니다:


```python hl_lines="1"
@api.get("/employees/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    return employee
```
여기서 우리는 단순히 employee ORM 객체를 반환했을 뿐, dictionary로 변환하지 않았습니다. `response` schema가 자동으로 결과를 검증하고 JSON으로 변환합니다:
```python hl_lines="4"
@api.get("/employees/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    return employee
```

### 객체 목록 가져오기
employee 목록을 출력하려면 동일한 `EmployeeOut` schema를 재사용할 수 있습니다. response schema를 `EmployeeOut`의 *List*로 설정하기만 하면 됩니다.
```python hl_lines="3"
from typing import List

@api.get("/employees", response=List[EmployeeOut])
def list_employees(request):
    qs = Employee.objects.all()
    return qs
```

또 한 가지 멋진 트릭 — 우리는 Django ORM queryset을 그대로 반환했다는 점에 유의하세요:

```python hl_lines="4"
@api.get("/employees", response=List[EmployeeOut])
def list_employees(request):
    qs = Employee.objects.all()
    return qs
```
queryset은 자동으로 평가되고, 검증되며, JSON 목록으로 변환됩니다!



## U: Update

업데이트는 꽤 간단합니다. `PUT` 메서드를 사용하면서 동시에 `employee_id`를 전달하기만 하면 됩니다:

```python hl_lines="1"
@api.put("/employees/{employee_id}")
def update_employee(request, employee_id: int, payload: EmployeeIn):
    employee = get_object_or_404(Employee, id=employee_id)
    for attr, value in payload.dict().items():
        setattr(employee, attr, value)
    employee.save()
    return {"success": True}
```

**참고**

여기서는 `payload.dict` 메서드를 사용하여 객체의 모든 속성을 설정했습니다:

`for attr, value in payload.dict().items()`

다음과 같이 명시적으로 작성할 수도 있습니다:

```python
employee.first_name = payload.first_name
employee.last_name = payload.last_name
employee.department_id = payload.department_id
employee.birthdate = payload.birthdate
```

**부분 업데이트(Partial updates)**

사용자가 부분 업데이트를 수행할 수 있게 하려면 `payload.dict(exclude_unset=True).items()`를 사용하세요. 이렇게 하면 지정된 필드만 업데이트됩니다.

**엄격한 필드 검증 강제하기**

기본적으로 schema에 존재하지 않는 제공된 필드는 조용히 무시됩니다. 그런 유효하지 않은 필드에 대해 에러를 발생시키려면, schema의 Config 클래스에 `extra = "forbid"`를 설정할 수 있습니다. 예를 들어:

```python hl_lines="4 5"
class EmployeeIn(Schema):
    # your fields here...

    class Config:
        extra = "forbid"
```

## D: Delete

삭제도 꽤 간단합니다. `id`로 employee를 가져와서 데이터베이스에서 제거하기만 하면 됩니다:


```python hl_lines="1 2 4"
@api.delete("/employees/{employee_id}")
def delete_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    return {"success": True}
```

## 최종 코드

완전한 CRUD 예제는 다음과 같습니다:


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

    튜토리얼이 여기서 끝입니다! 더 많은 정보는 **[How-to 가이드](../../guides/input/operations.md)**를 확인하세요.

    Django Ninja를 둘러싼 생태계:

    1. [django-ninja-crud](../../django-ninja-crud/index.md): django-ninja 위에 구축되어 CRUD 인터페이스 개발을 단순화하고, 선언적 model viewset과 시나리오 기반 테스트 방법을 제공하는 프레임워크입니다.

    2. [django-ninja-extra](../../django-ninja-extra/index.md): 개발자가 방대한 Django 문서를 건너뛰고 최소한의 코드로 강력한 웹 애플리케이션과 현대적인 API 인터페이스를 빠르게 구축할 수 있게 해주는 도구입니다.

    3. [django-ninja-jwt](../../django-ninja-jwt/index.md): django-ninja를 위한 JSON Web Token 플러그인으로, 인증 및 관련 기능을 구현하며 인기 있는 Django Rest Framework 플러그인에서 포크되었습니다.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
