---
comments: true
---
## Pendahuluan

Sejak **versi 3.1**, Django dilengkapi dengan **dukungan view asinkron**. Ini memungkinkan Anda menjalankan view konkuren yang efisien untuk beban kerja yang terikat jaringan dan/atau I/O.

```
pip install Django>=3.1 django-ninja
```

View asinkron bekerja lebih efisien ketika:
- Memanggil API eksternal melalui jaringan
- Menjalankan/menunggu query database
- Membaca/menulis ke disk

**Django Ninja** sepenuhnya mendukung view asinkron dan membuatnya sangat mudah digunakan.

## Contoh singkat

### Kode

Mari kita ambil sebuah contoh. Kita memiliki operasi API yang melakukan suatu pekerjaan (untuk saat ini, hanya sleep selama sejumlah detik tertentu) dan mengembalikan sebuah kata:
```python hl_lines="5"
import time

@api.get("/say-after")
def say_after(request, delay: int, word: str):
    time.sleep(delay)
    return {"saying": word}
```

Untuk menjalankan kode ini secara asinkron, yang perlu Anda lakukan hanyalah menambahkan keyword **`async`** ke fungsi tersebut (dan menggunakan library yang mendukung async untuk pekerjaannya - dalam kasus ini kita mengganti `sleep` dari standard library dengan `asyncio.sleep`):

```python hl_lines="1 4 5"
import asyncio

@api.get("/say-after")
async def say_after(request, delay: int, word: str):
    await asyncio.sleep(delay)
    return {"saying": word}
```

### Menjalankan

Untuk menjalankan kode ini, Anda memerlukan server ASGI seperti <a href="https://www.uvicorn.org/" target="_blank">Uvicorn</a> atau <a href="https://github.com/django/daphne" target="_blank">Daphne</a>. Di sini kita akan menggunakan Uvicorn, contohnya seperti di bawah ini:

Untuk menginstal Uvicorn, gunakan:

```
pip install uvicorn
```

Kemudian jalankan servernya:

```
uvicorn your_project.asgi:application --reload
```

> <small>
> *Catatan: ganti `your_project` dengan nama package proyek Anda*<br>
> *Flag `--reload` digunakan untuk memuat ulang server secara otomatis setiap kali Anda melakukan perubahan pada kode (jangan digunakan di production)*
> </small>

!!! note
    Anda dapat menjalankan view asinkron dengan `manage.py runserver`, tetapi cara ini tidak berjalan baik dengan beberapa library, jadi untuk saat ini (Juli 2020) disarankan menggunakan server ASGI seperti Uvicorn atau Daphne.

### Menguji

Buka <a href="http://127.0.0.1:8000/api/say-after?delay=3&word=hello" target="_blank">http://127.0.0.1:8000/api/say-after?delay=3&word=hello</a> (**delay=3**) di browser Anda.
Setelah menunggu 3 detik, Anda akan melihat pesan "hello".

Sekarang mari kita banjiri operasi ini dengan **100 request paralel**:

```
ab -c 100 -n 100 "http://127.0.0.1:8000/api/say-after?delay=3&word=hello"
```

Ini akan menghasilkan sesuatu seperti ini:

```
Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    1   1.1      1       4
Processing:  3008 3063  16.2   3069    3082
Waiting:     3008 3062  15.7   3068    3079
Total:       3008 3065  16.3   3070    3083

Percentage of the requests served within a certain time (ms)
  50%   3070
  66%   3072
  75%   3075
  80%   3076
  90%   3081
  95%   3082
  98%   3083
  99%   3083
 100%   3083 (longest request)
```

Berdasarkan angka-angka ini, service kita mampu menangani 100 request konkuren ini hanya dengan overhead yang sangat kecil.

Untuk mencapai konkurensi yang sama dengan WSGI dan operasi sinkron, Anda perlu menjalankan sekitar 10 workers dengan masing-masing 10 threads!

## Mencampur operasi sinkron dan asinkron

Perlu diingat bahwa Anda dapat **menggunakan operasi sync dan async sekaligus** di proyek Anda, dan **Django Ninja** akan mengarahkannya secara otomatis:

```python hl_lines="2 7"

@api.get("/say-sync")
def say_after_sync(request, delay: int, word: str):
    time.sleep(delay)
    return {"saying": word}

@api.get("/say-async")
async def say_after_async(request, delay: int, word: str):
    await asyncio.sleep(delay)
    return {"saying": word}
```

## Contoh Elasticsearch

Mari kita lihat use case di dunia nyata. Untuk contoh ini, mari gunakan versi terbaru Elasticsearch yang dilengkapi dukungan async:
```
pip install elasticsearch>=7.8.0
```

Sekarang, alih-alih menggunakan class `Elasticsearch`, gunakan class `AsyncElasticsearch` dan `await` hasilnya:

```python hl_lines="2 7 11 12"
from ninja import NinjaAPI
from elasticsearch import AsyncElasticsearch


api = NinjaAPI()

es = AsyncElasticsearch()


@api.get("/search")
async def search(request, q: str):
    resp = await es.search(
        index="documents", 
        body={"query": {"query_string": {"query": q}}},
        size=20,
    )
    return resp["hits"]
```

## Menggunakan ORM

Saat ini, beberapa bagian penting Django belum dapat beroperasi dengan aman di lingkungan asinkron karena memiliki global state yang tidak coroutine-aware. Bagian-bagian Django ini diklasifikasikan sebagai "asynchronous-unsafe" dan dilindungi dari eksekusi di lingkungan asinkron. **ORM** adalah contoh utamanya, tetapi ada bagian lain yang juga dilindungi dengan cara ini.
Pelajari lebih lanjut tentang async safety di <a href="https://docs.djangoproject.com/en/stable/topics/async/#async-safety" target="_blank">dokumentasi resmi Django</a>.

Jadi jika Anda melakukan ini:

```python hl_lines="3"
@api.get("/blog/{post_id}")
async def search(request, post_id: int):
    blog = Blog.objects.get(pk=post_id)
    ...
```

Akan muncul error. Sampai implementasi async ORM tersedia, Anda dapat menggunakan adapter `sync_to_async()`:

```python hl_lines="1 3 9"
from asgiref.sync import sync_to_async

@sync_to_async
def get_blog(post_id):
    return Blog.objects.get(pk=post_id)

@api.get("/blog/{post_id}")
async def search(request, post_id: int):
    blog = await get_blog(post_id)
    ...
```

Atau bahkan lebih singkat:

```python hl_lines="3"
@api.get("/blog/{post_id}")
async def search(request, post_id: int):
    blog = await sync_to_async(Blog.objects.get)(pk=post_id)
    ...
```

Ada satu **jebakan** yang umum terjadi: Django querysets dievaluasi secara lazy (query database hanya terjadi ketika Anda mulai mengiterasinya), jadi ini **tidak** akan berfungsi:

```python
all_blogs = await sync_to_async(Blog.objects.all)()
# ini akan melempar error nanti ketika Anda mencoba mengiterasi all_blogs
...
```

Sebagai gantinya, paksa evaluasinya (dengan `list`):

```python
all_blogs = await sync_to_async(list)(Blog.objects.all())
...
```

Sejak Django **versi 4.1**, Django dilengkapi dengan versi asinkron dari operasi-operasi ORM.
Ini menghilangkan kebutuhan untuk menggunakan `sync_to_async` dalam kebanyakan kasus.
Operasi asinkron memiliki nama yang sama dengan padanan sinkronnya, tetapi diawali huruf *a*. Jadi menggunakan contoh di atas,
Anda dapat menulisnya ulang menjadi:

```python hl_lines="3"
@api.get("/blog/{post_id}")
async def search(request, post_id: int):
    blog = await Blog.objects.aget(pk=post_id)
    ...
```

Saat bekerja dengan querysets, gunakan `async for` yang dipadukan dengan list comprehension:

```python
all_blogs = [blog async for blog in Blog.objects.all()]
...
```

Pelajari lebih lanjut tentang antarmuka ORM asinkron di <a href="https://docs.djangoproject.com/en/4.1/releases/4.1/#asynchronous-orm-interface" target="_blank">dokumentasi resmi Django</a>.

!!! success

    Lanjutkan ke bagian berikutnya **[Versioning API](versioning.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
