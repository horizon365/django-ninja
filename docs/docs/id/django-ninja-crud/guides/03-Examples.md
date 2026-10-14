---
comments: true
---
# Contoh Cepat
## 🌞 Cara Kerjanya

Mari bayangkan Anda sedang membangun sebuah sistem untuk sebuah universitas, dan Anda memiliki model bernama `Department`. Setiap departemen di universitas Anda memiliki judul yang unik.

```python
# examples/models.py
from django.db import models

class Department(models.Model):
    title = models.CharField(max_length=255, unique=True)
```

Untuk berinteraksi dengan data ini, kita membutuhkan cara untuk mengonversinya bolak-balik antara objek Python dan format yang mudah dibaca serta ditulis, seperti JSON. Di Django Ninja, kita menggunakan "Schema" untuk melakukan hal ini:

```python
# examples/schemas.py
from ninja import Schema

class DepartmentIn(Schema):
    title: str

class DepartmentOut(Schema):
    id: int
    title: str
```

Schema `DepartmentIn` mendefinisikan data yang kita butuhkan saat membuat atau memperbarui sebuah departemen. Schema `DepartmentOut` mendefinisikan data yang akan kita sediakan saat mengambil (retrieve) sebuah departemen.

Sekarang, di sinilah kekuatan package ini berperan. Dengan package ini, Anda dapat menyiapkan operasi **CRUD** untuk model `Department` hanya dalam beberapa baris kode:


```python
# examples/views/department_views.py
from typing import List
from django.http import HttpRequest
from ninja import NinjaAPI
from ninja_crud import views, viewsets

from examples.models import Department
from examples.schemas import DepartmentIn, DepartmentOut

api = NinjaAPI()


class DepartmentViewSet(viewsets.APIViewSet):
    api = api
    model = Department

    list_departments = views.ListView(
        response_body=List[DepartmentOut]
    )
    create_department = views.CreateView(
        request_body=DepartmentIn,
        response_body=DepartmentOut,
    )
    read_department = views.ReadView(
        response_body=DepartmentOut
    )
    update_department = views.UpdateView(
        request_body=DepartmentIn,
        response_body=DepartmentOut,
    )
    delete_department = views.DeleteView()


# In addition to the CRUD operations managed by the viewset,
# the api or router can be used in the standard Django Ninja way
@api.get("/statistics/", response=dict)
def get_department_statistics(request: HttpRequest):
    return {"total": Department.objects.count()}
```

Dan jika viewset Anda sederhana seperti di atas, Anda dapat memanfaatkan class `APIViewSet` untuk mendefinisikannya dengan cara yang lebih rapi, dengan request dan response body default:
```python
# examples/views/department_views.py
from ninja import NinjaAPI
from ninja_crud import views, viewsets

from examples.models import Department
from examples.schemas import DepartmentIn, DepartmentOut

api = NinjaAPI()


class DepartmentViewSet(viewsets.APIViewSet):
    api = api
    model = Department
    default_request_body = DepartmentIn
    default_response_body = DepartmentOut

    list_departments = views.ListView()
    create_department = views.CreateView()
    read_department = views.ReadView()
    update_department = views.UpdateView()
    delete_department = views.DeleteView()
```

## ☔️ Testing Berbasis Skenario

Django Ninja CRUD berintegrasi secara mulus dengan [Django REST Testing](https://github.com/hbakri/django-rest-testing), dan memastikan cakupan yang komprehensif serta validasi yang kokoh atas endpoint CRUD Anda.
Awalnya, framework testing ini merupakan bagian dari package ini, tetapi kemudian diekstrak menjadi package tersendiri untuk memberikan fleksibilitas lebih dan agar dapat digunakan dengan framework Django REST lain selain Django Ninja.

Dengan package ini, Anda dapat:
- **Mendefinisikan skenario test secara deklaratif**: tentukan detail request dan response yang diharapkan untuk setiap skenario, sehingga test Anda menjadi self-documenting dan mudah dipahami.
- **Menguji berbagai kondisi luas**: validasi perilaku endpoint di bawah berbagai kondisi, termasuk input valid dan tidak valid, resource yang tidak ada, dan aturan bisnis kustom.
- **Meningkatkan kejelasan dan maintainability**: pecah test menjadi unit yang modular dan mudah dikelola, meningkatkan organisasi kode dan mengurangi technical debt.
- **Memastikan cakupan komprehensif**: uji endpoint Anda secara ketat berkat pendekatan berbasis skenario, tanpa ada kasus yang tidak teruji.

Untuk menangani exception seperti `ObjectDoesNotExist` di test Anda dan mengembalikan respons yang sesuai, Anda dapat mendefinisikan exception handler seperti ini:

```python
# examples/exception_handlers.py
from ninja import NinjaAPI
from django.core.exceptions import ObjectDoesNotExist

api = NinjaAPI()


@api.exception_handler(ObjectDoesNotExist)
def handle_object_does_not_exist(request, exc):
    return api.create_response(
        request,
        {"message": "ObjectDoesNotExist", "detail": str(exc)},
        status=404,
    )

# ... other exception handlers
```

Sekarang, Anda dapat menulis test untuk view CRUD Anda menggunakan framework testing berbasis skenario:

```python
# examples/tests/test_department_views.py
from examples.models import Department
from examples.schemas import DepartmentOut

from ninja_crud.testing import APITestCase, APIViewTestScenario


class TestDepartmentViewSet(APITestCase):
    department: Department

    @classmethod
    def setUpTestData(cls):
        cls.department = Department.objects.create(title="department")

    def test_read_department(self):
        self.assertScenariosSucceed(
            method="GET",
            path="/api/departments/{id}",
            scenarios=[
                APIViewTestScenario(
                    path_parameters={"id": self.department.id},
                    expected_response_status=200,
                    expected_response_body_type=DepartmentOut,
                    expected_response_body={
                        "id": self.department.id,
                        "title": self.department.title,
                    },
                ),
                APIViewTestScenario(
                    path_parameters={"id": 9999},
                    expected_response_status=404,
                ),
            ],
        )
```

Dengan mengombinasikan view deklaratif milik Django Ninja CRUD dengan kemampuan testing berbasis skenario dari Django REST Testing, Anda dapat dengan mudah dan percaya diri membangun serta memelihara RESTful API yang kokoh dan teruji dengan baik.
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
