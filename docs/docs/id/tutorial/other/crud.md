---
comments: true
---
# Contoh CRUD (Create, Read, Update, Delete)


**CRUD** - **C**reate, **R**etrieve, **U**pdate, **D**elete adalah empat fungsi dasar dari persistent storage.

Contoh ini akan menunjukkan kepada Anda cara mengimplementasikan fungsi-fungsi tersebut dengan **Django Ninja**.

Misalkan Anda memiliki model Django berikut yang ingin Anda lakukan operasi-operasi tersebut:


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

Sekarang mari kita buat operasi CRUD untuk Employee.

## C: Create

Untuk membuat objek employee, Anda perlu mendefinisikan schema input:

```python
from datetime import date
from ninja import Schema

class EmployeeIn(Schema):
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None

```

Schema ini akan menjadi payload masukan kita:

```python hl_lines="2"
@api.post("/employees")
def create_employee(request, payload: EmployeeIn):
    employee = Employee.objects.create(**payload.dict())
    return {"id": employee.id}
```

!!! tip
    Objek `Schema` memiliki method `.dict()`, dengan semua atribut schema direpresentasikan sebagai dictionary.

    Anda dapat meneruskannya sebagai `**kwargs` ke method `create` model Django (atau `__init__` milik model).

Lihat snippet di bawah ini untuk menangani upload file (melalui form model Django):

```python hl_lines="2"
from ninja import UploadedFile, File

@api.post("/employees")
def create_employee(request, payload: EmployeeIn, cv: UploadedFile = File(...)):
    payload_dict = payload.dict()
    employee = Employee(**payload_dict)
    employee.cv.save(cv.name, cv) # will save model instance as well
    return {"id": employee.id}
```

Jika Anda hanya perlu mengunggah satu file:

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

### Objek tunggal

Sekarang, untuk mengambil objek employee, kita akan mendefinisikan sebuah schema yang akan mendeskripsikan seperti apa response kita nantinya. Di sini, kita pada dasarnya akan menggunakan schema yang sama dengan `EmployeeIn`, tetapi dengan properti `id` tambahan:

```python hl_lines="2"
class EmployeeOut(Schema):
    id: int
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None
```

!!! note
    Mendefinisikan schema response tidak sepenuhnya diwajibkan, tetapi ketika Anda melakukannya, Anda mendapatkan validasi hasil, dokumentasi, dan konversi otomatis objek ORM ke JSON.
Kita akan menggunakan schema ini sebagai tipe `response` dari view `GET` kita untuk mengambil seorang employee:


```python hl_lines="1"
@api.get("/employees/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    return employee
```
Perhatikan bahwa kita cukup mengembalikan objek ORM employee, tanpa mengonversinya menjadi dictionary. Schema `response` akan secara otomatis memvalidasi hasilnya dan mengonversinya ke JSON:
```python hl_lines="4"
@api.get("/employees/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    return employee
```

### Mendapatkan daftar objek
Untuk menampilkan daftar employee, kita dapat menggunakan kembali schema `EmployeeOut` yang sama. Kita hanya perlu mengatur schema response menjadi *List* dari `EmployeeOut`.
```python hl_lines="3"
from typing import List

@api.get("/employees", response=List[EmployeeOut])
def list_employees(request):
    qs = Employee.objects.all()
    return qs
```

Trik keren lainnya — perhatikan bahwa kita cukup mengembalikan sebuah queryset ORM Django:

```python hl_lines="4"
@api.get("/employees", response=List[EmployeeOut])
def list_employees(request):
    qs = Employee.objects.all()
    return qs
```
Queryset akan otomatis dievaluasi, divalidasi, dan dikonversi menjadi sebuah JSON list!



## U: Update

Melakukan update cukup sederhana. Kita hanya menggunakan method `PUT` dan meneruskan `employee_id` sekaligus:

```python hl_lines="1"
@api.put("/employees/{employee_id}")
def update_employee(request, employee_id: int, payload: EmployeeIn):
    employee = get_object_or_404(Employee, id=employee_id)
    for attr, value in payload.dict().items():
        setattr(employee, attr, value)
    employee.save()
    return {"success": True}
```

**Catatan**

Di sini kita menggunakan method `payload.dict` untuk mengatur semua atribut objek:

`for attr, value in payload.dict().items()`

Anda juga dapat menulisnya secara eksplisit seperti ini:

```python
employee.first_name = payload.first_name
employee.last_name = payload.last_name
employee.department_id = payload.department_id
employee.birthdate = payload.birthdate
```

**Update parsial**

Untuk memungkinkan user melakukan update parsial, gunakan `payload.dict(exclude_unset=True).items()`. Ini memastikan bahwa hanya field yang ditentukan saja yang akan diperbarui.

**Menerapkan validasi field yang ketat**

Secara default, field apa pun yang disediakan tetapi tidak ada di schema akan diabaikan secara diam-diam. Untuk menimbulkan error bagi field tidak valid tersebut, Anda dapat mengatur `extra = "forbid"` di class Config milik schema. Sebagai contoh:

```python hl_lines="4 5"
class EmployeeIn(Schema):
    # your fields here...

    class Config:
        extra = "forbid"
```

## D: Delete

Menghapus juga cukup sederhana. Kita hanya mengambil employee berdasarkan `id` dan menghapusnya dari database:


```python hl_lines="1 2 4"
@api.delete("/employees/{employee_id}")
def delete_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    return {"success": True}
```

## Kode akhir

Berikut adalah contoh CRUD yang lengkap:


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

    Ini adalah akhir dari tutorial! Lihat **[Panduan how-to](../../guides/input/operations.md)** untuk informasi lebih lanjut.

    Ekosistem di sekitar Django Ninja:

    1. [django-ninja-crud](../../django-ninja-crud/index.md): Framework yang dibangun di atas django-ninja untuk menyederhanakan pengembangan antarmuka CRUD, menyediakan model viewset deklaratif dan metode pengujian berbasis skenario.

    2. [django-ninja-extra](../../django-ninja-extra/index.md): Alat yang memungkinkan developer melewati dokumentasi Django yang bertele-tele dan membangun aplikasi web yang powerful serta antarmuka API modern dengan kode minimal.

    3. [django-ninja-jwt](../../django-ninja-jwt/index.md): Plugin JSON Web Token untuk django-ninja yang mengimplementasikan authentication dan fitur terkait, di-fork dari plugin Django Rest Framework yang populer.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
