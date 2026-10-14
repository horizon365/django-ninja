---
comments: true
---
# Query Parameters

Ketika Anda mendeklarasikan function parameters yang bukan bagian dari path parameters, parameter tersebut secara otomatis ditafsirkan sebagai "query" parameters.
```python hl_lines="5"
{!./src/tutorial/query/code01.py!}
```

Untuk mem-query operation ini, Anda dapat menggunakan URL seperti ini:

```
http://localhost:8000/api/weapons?offset=0&limit=10
```
Secara default, semua parameter GET adalah string; ketika Anda menganotasi function parameters Anda dengan tipe, parameter tersebut akan dikonversi ke tipe tersebut dan divalidasi terhadapnya.

Manfaat yang sama seperti pada path parameters juga berlaku untuk query parameters:

- Dukungan editor (tentu saja)
- "Parsing" data
- Validasi data
- Dokumentasi otomatis


!!! note
    Jika Anda tidak menganotasi parameter Anda, parameter tersebut akan diperlakukan bertipe `str`

```python hl_lines="2"
@api.get("/weapons")
def list_weapons(request, limit, offset):
    # type(limit) == str
    # type(offset) == str
```

### Nilai Default

Karena query parameters bukan bagian tetap dari path, parameter tersebut bersifat opsional dan dapat memiliki nilai default:

```python hl_lines="2"
@api.get("/weapons")
def list_weapons(request, limit: int = 10, offset: int = 0):
    return weapons[offset : offset + limit]
```

Dalam contoh di atas, kita menyetel nilai default `offset=0` dan `limit=10`.

Jadi, mengunjungi URL:
```
http://localhost:8000/api/weapons
```
akan sama dengan mengunjungi:
```
http://localhost:8000/api/weapons?offset=0&limit=10
```
Jika Anda mengunjungi, misalnya:
```
http://localhost:8000/api/weapons?offset=20
```

Nilai parameter di fungsi Anda akan menjadi:

 - `offset=20` (karena Anda menyetelnya di URL)
 - `limit=10` (karena itulah nilai defaultnya)


### Parameter Wajib dan Opsional

Anda dapat mendeklarasikan parameter GET yang wajib atau opsional dengan cara yang sama seperti Anda mendeklarasikan parameter fungsi Python:

```python hl_lines="5"
{!./src/tutorial/query/code02.py!}
```

Dalam kasus ini, **Django Ninja** akan selalu memvalidasi parameter `q` yang Anda kirimkan dalam request GET, sedangkan parameter `offset` adalah integer opsional.

### Konversi Tipe Parameter GET

Mari kita deklarasikan beberapa parameter bertipe:
```python hl_lines="5"
{!./src/tutorial/query/code03.py!}
```
Tipe `str` diteruskan apa adanya.

Untuk tipe `bool`, semua berikut ini:
```
http://localhost:8000/api/example?b=1
http://localhost:8000/api/example?b=True
http://localhost:8000/api/example?b=true
http://localhost:8000/api/example?b=on
http://localhost:8000/api/example?b=yes
```
atau variasi huruf lainnya (huruf besar, kapitalisasi awal, dll.), fungsi Anda akan melihat
bahwa parameter `b` memiliki nilai `bool` `True`, jika tidak maka `False`.

Tanggal dapat berupa string tanggal maupun integer (Unix timestamps):

<pre style="font-size: .85em; background-color:rgb(245, 245, 245);">
http://localhost:8000/api/example?d=<strong>1577836800</strong>  # equivalent to 2020-01-01
http://localhost:8000/api/example?d=<strong>2020-01-01</strong>
</pre>


### Menggunakan Schema

Anda juga dapat menggunakan schema untuk mengenkapsulasi parameter GET:

```python hl_lines="1 2  5 6 7 8"
{!./src/tutorial/query/code010.py!}
```

Untuk skenario filtering yang lebih kompleks, lihat [Filtering](./filtering.md).

!!! done

    Lanjutkan ke bab berikutnya! **[Request Body](body.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
