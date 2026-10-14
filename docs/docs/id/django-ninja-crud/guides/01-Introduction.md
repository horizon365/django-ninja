---
comments: true
---
# Pendahuluan
Django Ninja CRUD adalah framework yang powerful, [deklaratif](https://en.wikipedia.org/wiki/Declarative_programming), namun sedikit opinionated, yang menyederhanakan pengembangan endpoint **CRUD** ([**C**reate, **R**ead, **U**pdate, **D**elete](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete)) dengan [Django Ninja](https://github.com/vitalik/django-ninja),
dan juga menyediakan pendekatan deklaratif berbasis skenario untuk menguji endpoint API tersebut menggunakan [Django REST Testing](https://github.com/hbakri/django-rest-testing).

## 🍓 Mendefinisikan Ulang Model Viewsets CRUD yang Deklaratif  

Melangkahlah ke masa depan operasi CRUD Django dengan model viewsets kami. Framework kami memandang ulang pembuatan endpoint melalui lensa deklaratif, mengubah proses yang kompleks menjadi kode yang ringkas dan mudah dibaca. Dibangun di atas best practices, model viewsets merangkum esensi desain yang efisien dan kokoh. Dengan mendeklarasikan model dan schema, Anda dapat dengan cepat menghasilkan operasi CRUD yang lengkap, membebaskan Anda untuk menangani tantangan yang benar-benar penting. Di sinilah perjalanan mendefinisikan ulang pengembangan aplikasi web dimulai.
```python
from ninja import Router
from ninja_crud import views, viewsets

from examples.models import Department
from examples.schemas import DepartmentIn, DepartmentOut

router = Router()


class DepartmentViewSet(viewsets.ModelViewSet):
    model = Department
    default_input_schema = DepartmentIn
    default_output_schema = DepartmentOut

    list_view = views.ListModelView()
    create_view = views.CreateModelView()
    retrieve_view = views.RetrieveModelView()
    update_view = views.UpdateModelView()
    delete_view = views.DeleteModelView()


DepartmentViewSet.register_routes(router)
```
## Masalah yang Perlu Diselesaikan
Package ini memungkinkan Anda mendefinisikan endpoint umum sebagai class-based views dan dengan mudah mengkustomisasinya agar sesuai dengan konvensi project Anda, serta dengan mudah membuat view kustom Anda sendiri dan mendeklarasikannya berdampingan dengan view CRUD yang disediakan, sehingga mendorong modularitas dan ekstensibilitas.
Package ini mendorong fokus pada hal yang paling penting: **menyelesaikan masalah dunia nyata**, alih-alih menemukan kembali roda di seluruh project Anda.

Awalnya terinspirasi oleh [ModelViewSet](https://www.django-rest-framework.org/api-guide/viewsets/#modelviewset) milik DRF,
Django Ninja CRUD berevolusi untuk mengatasi keterbatasannya, mengadopsi pendekatan [composition over inheritance](https://en.wikipedia.org/wiki/Composition_over_inheritance)
untuk mencapai modularitas sejati — langkah dasar menuju pendekatan deklaratif yang lebih luas untuk membuat endpoint API.

Tantangan yang dihadapi viewsets berbasis inheritance yang ada:

- **Keunikan endpoint CRUD per model**: Django Ninja CRUD memungkinkan Anda mendefinisikan beberapa endpoint untuk model yang sama, memungkinkan versioning atau representasi alternatif.    
- **Kurangnya fleksibilitas kustomisasi**: alih-alih meng-override metode pada satu class monolitik, masing-masing view dapat dikustomisasi melalui composition dan konfigurasi.         
- **Hubungan implisit dalam hierarki inheritance**: composition memisahkan (decouple) view-view, mengurangi dependensi dan meningkatkan reusability.       
- **Kurangnya modularitas untuk endpoint baru**: menambahkan endpoint kustom tidak lagi memerlukan subclassing dari seluruh viewset, sehingga lebih mudah memperkenalkan fitur baru secara bertahap.      

## ✨ Fitur Utama
- **Murni deklaratif**: definisikan view dan test dengan mendeklarasikan apa yang Anda inginkan, bukan bagaimana melakukannya.
- **Modularitas tak tertandingi**: kustomisasi viewset Anda dengan view CRUD yang diinginkan, mengkustomisasi perilaku setiap view.
- **Framework testing berbasis skenario**: manfaatkan framework testing berbasis skenario untuk mendefinisikan beragam test case secara deklaratif dan ringkas.
- **Fokus pada hal yang penting**: habiskan lebih banyak waktu untuk menyelesaikan masalah dunia nyata dan lebih sedikit untuk tugas-tugas umum yang repetitif.

> Menguji secara presisi dengan test case model viewset

```python
from ninja_crud import testing

from examples.models import Department
from examples.views import DepartmentViewSet


class TestDepartmentViewSet(testing.viewsets.ModelViewSetTestCase):
    model_viewset_class = DepartmentViewSet
    base_path = "api/departments"

    @classmethod
    def setUpTestData(cls):
        cls.department_1 = Department.objects.create(title="department-1")
        cls.department_2 = Department.objects.create(title="department-2")

    @property
    def path_parameters(self):
        return testing.components.PathParameters(
            ok={"id": self.department_1.id},
            not_found={"id": 999}
        )

    @property
    def payloads(self):
        return testing.components.Payloads(
            ok={"title": "department-3"},
            bad_request={"title": ""},
            conflict={"title": self.department_2.title}
        )

    test_list_view = testing.views.ListModelViewTest()
    test_create_view = testing.views.CreateModelViewTest(payloads)
    test_retrieve_view = testing.views.RetrieveModelViewTest(path_parameters)
    test_update_view = testing.views.UpdateModelViewTest(path_parameters, payloads)
    test_delete_view = testing.views.DeleteModelViewTest(path_parameters)

```

**Django Ninja CRUD lebih dari sekadar tool; ia adalah pergeseran paradigma dalam pengembangan dan testing aplikasi web Django.**



## 💬 Selanjutnya?


!!! success

    Lanjutkan ke bab berikutnya **[Cara Install](02-Installation.md)**.
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
