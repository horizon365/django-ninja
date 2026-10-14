---
comments: true
---
# Request Body

Request body biasanya digunakan dengan operasi "create" dan "update" (POST, PUT, PATCH).
Misalnya, saat membuat sebuah resource dengan POST atau PUT, request body biasanya berisi representasi dari resource yang akan dibuat.

Untuk mendeklarasikan request body, Anda perlu menggunakan **`Schema` milik Django Ninja**.

!!! note
    Di balik layar, **Django Ninja** memanfaatkan seluruh kekuatan dan fitur dari <a href="https://pydantic.com.cn/" class="external-link" target="_blank">Pydantic</a> Model.
    Alias `Schema` dipilih untuk menghindari kebingungan kode saat bekerja dengan Django models, karena class model milik Pydantic secara default bernama `Model`, yang bentrok dengan class `Model` milik Django.
    

## Mengimpor Schema

Pertama, Anda perlu mengimpor `Schema` dari `ninja`:

```python hl_lines="2"
{!./src/tutorial/body/code01.py!}
```

## Membuat Data Model Anda

Kemudian deklarasikan data model Anda sebagai class yang mewarisi dari `Schema`.

Gunakan tipe Python standar untuk semua atribut:

```python hl_lines="5 6 7 8 9"
{!./src/tutorial/body/code01.py!}
```

Catatan: jika Anda menyetel nilai default sebuah atribut menjadi **`None`**, atribut tersebut menjadi opsional dalam request body. Misalnya, model di atas mendeklarasikan sebuah "`object`" JSON (atau `dict` Python) seperti ini:

```JSON
{
    "name": "Katana",
    "description": "An optional description",
    "price": 299.00,
    "quantity": 10
}
```

...karena `description` bersifat opsional (nilai defaultnya `None`), JSON "`object`" berikut ini juga akan valid:

```JSON
{
    "name": "Katana",
    "price": 299.00,
    "quantity": 10
}
```

## Mendeklarasikannya sebagai Parameter

Untuk menambahkannya ke *path operation* Anda, deklarasikan dengan cara yang sama seperti Anda mendeklarasikan path dan query parameters:


```python hl_lines="13"
{!./src/tutorial/body/code01.py!}
```

... dan deklarasikan tipenya sebagai model `Item` yang Anda buat.

## Hasil

Hanya dengan deklarasi tipe Python tersebut, **Django Ninja** akan:

* Membaca request body sebagai JSON.
* Mengonversi ke tipe yang sesuai (bila diperlukan).
* Memvalidasi data.
    * Jika data tidak valid, akan dikembalikan error yang ramah dan informatif yang secara tepat menunjukkan lokasi dan isi data yang salah.
* Memberikan data yang diterima kepada Anda di parameter `item`.
    * Karena Anda mendeklarasikan tipenya sebagai `Item` di fungsi, Anda juga mendapatkan dukungan editor (autocomplete, dll.) untuk semua atribut dan tipenya.
* Menghasilkan definisi <a href="https://json-schema.org" class="external-link" target="_blank">JSON Schema</a> untuk model Anda, yang juga dapat Anda gunakan di mana saja sesuai kebutuhan dalam proyek Anda.
* Schema-schema tersebut akan menjadi bagian dari skema OpenAPI yang dihasilkan dan digunakan oleh <abbr title="User Interfaces">UI</abbr> dokumentasi otomatis.

## Dokumentasi otomatis

JSON Schema dari model-model Anda akan menjadi bagian dari skema OpenAPI yang dihasilkan dan ditampilkan dalam dokumentasi API interaktif:

![Openapi schema](../../img/body-schema-doc.png)

...dan juga akan digunakan dalam dokumentasi API untuk setiap *path operation* yang membutuhkannya:

![Openapi schema](../../img/body-schema-doc2.png)

## Dukungan Editor

Di editor Anda, di dalam fungsi, Anda akan mendapatkan type hints dan completion di mana saja (ini tidak akan terjadi jika Anda menggunakan `dict` alih-alih objek Schema):

![Type hints](../../img/body-editor.gif)


Screenshot sebelumnya menggunakan <a href="https://code.visualstudio.com" class="external-link" target="_blank">Visual Studio Code</a>.

Anda akan mendapatkan dukungan editor yang sama di <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a> dan sebagian besar editor Python lainnya.

## Request Body + Path Parameters

Anda dapat mendeklarasikan path parameters **dan** request body sekaligus.


**Django Ninja** akan mengenali bahwa function parameters yang cocok dengan path parameters harus diambil **dari path**, sedangkan function parameters yang dideklarasikan dengan `Schema` harus diambil **dari request body**.

```python hl_lines="11 12"
{!./src/tutorial/body/code02.py!}
```

## Request Body + Path + Query Parameters

Anda juga dapat mendeklarasikan **request body**, **path**, dan **query** parameters sekaligus.

**Django Ninja** akan mengenali setiap parameter dan mengambil data dari lokasi yang benar.

```python hl_lines="11 12"
{!./src/tutorial/body/code03.py!}
```

Function parameters akan dikenali sebagai berikut:

* Jika parameter juga dideklarasikan di **path**, parameter tersebut akan digunakan sebagai path parameter.

 
* Jika parameter bertipe **tunggal** (seperti `int`, `float`, `str`, `bool`, dll.), parameter tersebut akan ditafsirkan sebagai **query** parameter.
* Jika parameter dideklarasikan dengan tipe **Schema** (atau `BaseModel` Pydantic), parameter tersebut akan ditafsirkan sebagai **request body**.

!!! done

    Lanjutkan ke bab berikutnya! **[Form Data](form-params.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
