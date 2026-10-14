---
comments: true
---
# CRUD（Create, Read, Update, Delete）の例


**CRUD** - **C**reate（作成）、**R**etrieve（取得）、**U**pdate（更新）、**D**elete（削除）は、永続ストレージの 4 つの基本機能です。

この例では、**Django Ninja** を使ってこれらの機能を実装する方法を紹介します。

これらの操作を実行したい次の Django モデルがあるとします：


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

では、Employee に対する CRUD 操作を作成していきましょう。

## C: Create

従業員オブジェクトを作成するには、入力用の schema を定義する必要があります：

```python
from datetime import date
from ninja import Schema

class EmployeeIn(Schema):
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None

```

この schema が受け取るペイロードになります：

```python hl_lines="2"
@api.post("/employees")
def create_employee(request, payload: EmployeeIn):
    employee = Employee.objects.create(**payload.dict())
    return {"id": employee.id}
```

!!! tip
    `Schema` オブジェクトには `.dict()` メソッドがあり、すべての schema 属性が辞書として表現されます。

    それを `**kwargs` として Django モデルの `create` メソッド（またはモデルの `__init__`）に渡せます。

次のスニペットは、（Django モデルの form を介して）ファイルアップロードを処理する方法です：

```python hl_lines="2"
from ninja import UploadedFile, File

@api.post("/employees")
def create_employee(request, payload: EmployeeIn, cv: UploadedFile = File(...)):
    payload_dict = payload.dict()
    employee = Employee(**payload_dict)
    employee.cv.save(cv.name, cv) # will save model instance as well
    return {"id": employee.id}
```

単一のファイルをアップロードするだけなら：

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

### 単一オブジェクト

次に、従業員オブジェクトを取得するために、レスポンスの形を記述する schema を定義します。ここでは、基本的には `EmployeeIn` と同じ schema を使い、`id` プロパティを追加したものにします：

```python hl_lines="2"
class EmployeeOut(Schema):
    id: int
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None
```

!!! note
    レスポンススキーマの定義は厳密には必須ではありませんが、定義すれば結果の検証、ドキュメント化、ORM オブジェクトから JSON への自動変換が得られます。
この schema を、従業員を取得する `GET` ビューの `response` 型として使います：


```python hl_lines="1"
@api.get("/employees/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    return employee
```
従業員の ORM オブジェクトを、辞書に変換せずにそのまま返しただけであることに注目してください。`response` スキーマが結果を自動的に検証し、JSON に変換します：
```python hl_lines="4"
@api.get("/employees/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    return employee
```

### オブジェクトのリストを取得する
従業員のリストを出力するには、同じ `EmployeeOut` スキーマを再利用できます。レスポンススキーマを `EmployeeOut` の *List* に設定するだけです。
```python hl_lines="3"
from typing import List

@api.get("/employees", response=List[EmployeeOut])
def list_employees(request):
    qs = Employee.objects.all()
    return qs
```

もうひとつの便利なテクニック — Django ORM の queryset をそのまま返しただけであることに注目してください：

```python hl_lines="4"
@api.get("/employees", response=List[EmployeeOut])
def list_employees(request):
    qs = Employee.objects.all()
    return qs
```
これは自動的に評価、検証され、JSON のリストに変換されます！



## U: Update

更新はとてもシンプルです。`PUT` メソッドを使い、同時に `employee_id` を渡すだけです：

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

ここでは、オブジェクトのすべての属性を設定するために `payload.dict` メソッドを使いました：

`for attr, value in payload.dict().items()`

これを次のように明示的に書くこともできます：

```python
employee.first_name = payload.first_name
employee.last_name = payload.last_name
employee.department_id = payload.department_id
employee.birthdate = payload.birthdate
```

**部分更新**

ユーザーに部分更新を許可するには、`payload.dict(exclude_unset=True).items()` を使います。これにより、指定されたフィールドだけが更新されることが保証されます。

**厳格なフィールド検証の強制**

デフォルトでは、スキーマに存在しない指定フィールドは黙って無視されます。そのような無効なフィールドに対してエラーを発生させたい場合は、スキーマの Config クラスで `extra = "forbid"` を設定できます。たとえば：

```python hl_lines="4 5"
class EmployeeIn(Schema):
    # your fields here...

    class Config:
        extra = "forbid"
```

## D: Delete

削除もまたとてもシンプルです。`id` で従業員を取得し、データベースから削除するだけです：


```python hl_lines="1 2 4"
@api.delete("/employees/{employee_id}")
def delete_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    return {"success": True}
```

## 最終コード

CRUD の完全な例は次のとおりです：


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

    これでチュートリアルは終わりです！ 詳しくは **[ハウツーガイド](../../guides/input/operations.md)** をチェックしてください。

    Django Ninja を取り巻くエコシステム：

    1. [django-ninja-crud](../../django-ninja-crud/index.md): django-ninja をベースに構築された、CRUD インターフェースの開発を簡素化するフレームワーク。宣言的なモデルビューセットとシナリオベースのテスト手法を提供します。

    2. [django-ninja-extra](../../django-ninja-extra/index.md): 冗長な Django ドキュメントを読み飛ばし、最小限のコードで強力な Web アプリケーションとモダンな API インターフェースを素早く構築できるツールです。

    3. [django-ninja-jwt](../../django-ninja-jwt/index.md): django-ninja 向けの JSON Web Token プラグイン。認証および関連機能を実装しており、人気の高い Django Rest Framework プラグインからフォークされました。

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
