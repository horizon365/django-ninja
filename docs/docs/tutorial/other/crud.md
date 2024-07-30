---
comments: true
---
# CRUD（增删改查）例子


**CRUD**  - **C**reate, **R**etrieve, **U**pdate, **D**elete （增删改查）是持久存储的四项基本功能。

这个示例将向你展示如何用 **Django Ninja** 来实现这些功能。

假设你有以下需要对其执行这些操作的 Django 模型：


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

现在让我们来对 Employee 创建 CRUD 操作。

## C: 创建

创建一个 employee 对象的话，需要定义一个输入 schema:

```python
from datetime import date
from ninja import Schema

class EmployeeIn(Schema):
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None

```

这个 schema 将是我们的传入的 payload:

```python hl_lines="2"
@api.post("/employees")
def create_employee(request, payload: EmployeeIn):
    employee = Employee.objects.create(**payload.dict())
    return {"id": employee.id}
```

!!! tip
    `Schema` 对象有 `.dict()` 方法，所有模式属性都表示为一个字典。

    你可以传递它作为 `**kwargs` 给到 Django 模型的`create` 方法 (或模型的 `__init__`).

参考下面的代码片段去处理文件上传 (通过 Django models 的形式):

```python hl_lines="2"
from ninja import UploadedFile, File

@api.post("/employees")
def create_employee(request, payload: EmployeeIn, cv: UploadedFile = File(...)):
    payload_dict = payload.dict()
    employee = Employee(**payload_dict)
    employee.cv.save(cv.name, cv) # will save model instance as well
    return {"id": employee.id}
```

如果你仅仅需要上传一个文件:

```python hl_lines="2"
from django.core.files.storage import FileSystemStorage
from ninja import UploadedFile, File

STORAGE = FileSystemStorage()

@api.post("/upload")
def create_upload(request, cv: UploadedFile = File(...)):
    filename = STORAGE.save(cv.name, cv)
    # Handle things further
```

## R: 查

### 单个对象

现在为了获取 employee 对象，我们将定义一个模式，它将描述我们的响应会是什么样子。在这里，我们基本上将使用与 `EmployeeIn` 相同的模式，但会添加一个额外的属性 `id`：

```python hl_lines="2"
class EmployeeOut(Schema):
    id: int
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None
```

!!! 注意
    定义响应模式并非真正必需的，但当你进行定义时，你将获得结果验证、文档以及自动将 ORM 对象转换为 JSON 的功能。
我们将把这个模式用作我们使用 `GET` 方式获取 employee 视图的 `响应` 类型：


```python hl_lines="1"
@api.get("/employees/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    return employee
```
请注意，我们只是简单地返回了一个员工 ORM 对象，无需将其转换为字典。`响应` 模式会自动进行结果验证并转换为 JSON：
```python hl_lines="4"
@api.get("/employees/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    return employee
```

### 获取对象列表
要输出 employees 的列表，我们可以复用相同的 `EmployeeOut` 模式。我们只需将响应模式设置为 `EmployeeOut` 的*List*。
```python hl_lines="3"
from typing import List

@api.get("/employees", response=List[EmployeeOut])
def list_employees(request):
    qs = Employee.objects.all()
    return qs
```

另一个很酷的技巧 - 注意我们只是返回了一个 Django ORM 查询集：

```python hl_lines="4"
@api.get("/employees", response=List[EmployeeOut])
def list_employees(request):
    qs = Employee.objects.all()
    return qs
```
它会自动被求值、验证并转换为 JSON 列表！



## U: 更新

更新相当简单。我们只需使用 `PUT` 方法并同时传递 `employee_id`:

```python hl_lines="1"
@api.put("/employees/{employee_id}")
def update_employee(request, employee_id: int, payload: EmployeeIn):
    employee = get_object_or_404(Employee, id=employee_id)
    for attr, value in payload.dict().items():
        setattr(employee, attr, value)
    employee.save()
    return {"success": True}
```

**注意**

在这里我们使用了 `payload.dict` 方法来设置所有对象的属性:

`for attr, value in payload.dict().items()`

你也可以明确的写成这样:

```python
employee.first_name = payload.first_name
employee.last_name = payload.last_name
employee.department_id = payload.department_id
employee.birthdate = payload.birthdate
```

**部分更新**

为了允许用户进行部分更新，使用 `payload.dict(exclude_unset=True).items()`。这确保了只有指定的字段会被更新。

**强制严格字段验证**

默认情况下，任何提供的不存在于模式中的字段将被静默忽略。要对这些无效字段引发错误，你可以在模式的 Config 类中设置 `extra = "forbid"`。例如：

```python hl_lines="4 5"
class EmployeeIn(Schema):
    # your fields here...

    class Config:
        extra = "forbid"
```

## D: 删除

删除也相当简单。我们只需通过 `id` 获取员工并从数据库中删除它：


```python hl_lines="1 2 4"
@api.delete("/employees/{employee_id}")
def delete_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    return {"success": True}
```

## 最终代码

这是一个完整的 CRUD 示例：


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

!!! 大功告成

    本教程到此结束！查看 **[How-to 系列](../../guides/input/operations.md)** 以获取更多信息。
    
    Django ninja 周边生态： 

    1. [django-ninja-crud](../../django-ninja-crud/index.md) : 是一个基于django-ninja来简化CRUD接口开发的框架，提供声明式的模型视图集及基于场景的测试方法。

    2. [django-ninja-extra](../../django-ninja-extra/index.md) : 是一个可以让开发者摆脱冗长Django文档，仅用少量代码就能快速构建强大Web应用和现代API接口的工具。

    3. [django-ninja-jwt](../../django-ninja-jwt/index.md) : 为django-ninja提供的JSON Web Token插件，用于实现身份验证等相关功能，是从一个流行的Django Rest Framework插件分支而来。

<img style="object-fit: cover; object-position: 50% 50%;" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
