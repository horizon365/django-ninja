---
comments: true
---
# Motivasi

!!! note
    **Django Ninja** pada dasarnya terlihat sama dengan **FastAPI**, jadi mengapa tidak langsung menggunakan FastAPI?

Memang benar, **Django Ninja** sangat terinspirasi oleh <a href="https://fastapi.tiangolo.com/" target="_blank">FastAPI</a> (dikembangkan oleh <a href="https://github.com/tiangolo" target="_blank">Sebastián Ramírez</a>)

Meski begitu, ada beberapa masalah ketika membuat FastAPI dan Django bekerja bersama dengan benar:

1) **FastAPI** mengklaim bersifat ORM-agnostic (artinya Anda dapat menggunakannya dengan SQLAlchemy atau Django ORM), tetapi dalam praktiknya Django ORM belum siap untuk penggunaan async (mungkin pada versi 4.0 atau 4.1). Jika Anda menggunakannya dalam mode sinkron, Anda mungkin menghadapi [masalah koneksi yang tertutup](https://github.com/tiangolo/fastapi/issues/716) dan Anda perlu berusaha **sangat** keras untuk mengatasinya.

2) Ketika Anda bergantung pada authentication dan database session dalam operasi Anda (untuk beberapa proyek ini mencakup sekitar 99% dari semua operasi), dependency injection dengan parameter membuat kode Anda menjadi terlalu bertele-tele.

```python hl_lines="25 26"
...

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = decode(token)
    if not user:
        raise HTTPException(...)
    return user


@app.get("/task/{task_id}", response_model=Task)
def read_user(
        task_id: int,
        db: Session = Depends(get_db), 
        current_user: User = Depends(get_current_user),
    ):
        ... use db with current_user ....
```

3) Karena kata `model` sudah "direserved" di Django untuk digunakan oleh ORM, segalanya menjadi sangat berantakan ketika Anda mencampur konvensi penamaan model Django ORM dan Pydantic/FastAPI.

### Django Ninja

Django Ninja menyelesaikan semua masalah tersebut dan terintegrasi dengan sangat baik dengan Django (ORM, URLs, views, authentication, dll.).
Saat bekerja di [Code-on, sebuah studio desain dan pengembangan web Django](https://code-on.be/), saya menghadapi berbagai tantangan, dan untuk menjawabnya saya memulai proyek Django-Ninja pada tahun 2020.

Catatan: **Django Ninja adalah proyek yang siap untuk production** - saya memperkirakan saat ini lebih dari 100 perusahaan menggunakannya di production, dengan 500 developer baru bergabung setiap bulannya.

Beberapa perusahaan sudah mulai mencari developer dengan pengalaman Django Ninja.

#### Fitur utama

1) Karena Anda dapat memiliki beberapa instance API Django Ninja, Anda dapat menjalankan [beberapa versi API](guides/versioning.md) dalam satu proyek Django.

```python
api_v1 = NinjaAPI(version='1.0', auth=token_auth)
...
api_v2 = NinjaAPI(version='2.0', auth=token_auth)
...
api_private = NinjaAPI(auth=session_auth, urls_namespace='private_api')
...


urlpatterns = [
    ...
    path('api/v1/', api_v1.urls),
    path('api/v2/', api_v2.urls),
    path('internal-api/', api_private.urls),
]
```

2) Class 'Schema' milik Django Ninja terintegrasi dengan ORM, sehingga Anda dapat [menserialisasi queryset](guides/response/index.md#returning-querysets) atau objek ORM:

```python
@api.get("/tasks", response=List[TaskSchema])
def tasks(request):
    return Task.objects.all()


@api.get("/tasks", response=TaskSchema)
def tasks_details(request):
    task = Task.objects.first()
    return task
```
3) [Membuat Schema dari model Django](guides/response/django-pydantic.md).

4) Alih-alih menggunakan parameter dependency, **Django Ninja** menggunakan properti instance `request` (dengan cara yang sama seperti view Django pada umumnya) - lihat [Authentication](guides/authentication.md) untuk detail lebih lanjut.

!!! note

    Lihat **[Tutorial](tutorial/index.md)** untuk memulai dengan cepat.

    Ekosistem di sekitar Django Ninja:

    1. [django-ninja-crud](django-ninja-crud/index.md): Framework yang dibangun di atas django-ninja untuk menyederhanakan pengembangan antarmuka CRUD, menyediakan model viewset deklaratif dan metode pengujian berbasis skenario.

    2. [django-ninja-extra](django-ninja-extra/index.md): Alat yang memungkinkan developer melewati dokumentasi Django yang bertele-tele dan membangun aplikasi web yang powerful serta antarmuka API modern dengan kode minimal.

    3. [django-ninja-jwt](django-ninja-jwt/index.md): Plugin JSON Web Token untuk django-ninja yang mengimplementasikan authentication dan fitur terkait, di-fork dari plugin Django Rest Framework yang populer.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
