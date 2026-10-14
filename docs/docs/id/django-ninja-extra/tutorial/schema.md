---
comments: true
---
Integrasi Django-Ninja dengan Pydantic adalah salah satu fitur terbaik dari Django-Ninja.
Dengan Pydantic, Anda dapat memvalidasi data yang mengalir masuk dan keluar dari API Anda, dan prosesnya sangat cepat. Pydantic dapat menggantikan sebagian DRF serializers.

Tetapi jika Anda ingin menggantikan DRF serializers sepenuhnya, yang Anda butuhkan adalah **Ninja-Schema**.

## Ninja Schema

Ninja Schema mengubah model Django ORM Anda menjadi skema Pydantic yang mendukung lebih banyak fitur Pydantic.

**Inspirasi**: [django-ninja](https://django-ninja.cn/) dan [djantic](https://jordaneremieff.github.io/djantic/)

**Fitur Utama:**

- **Dukungan Custom Field**: Ninja Schema mengubah model Django menjadi tipe Pydantic native, yang memungkinkan Anda mendapatkan validasi field yang cepat secara langsung. Contohnya termasuk enum, email, alamat IP, URL, JSON, dan lainnya.
- **Validator Field**: Field dapat divalidasi menggunakan **model_validator**, sama seperti **[validator](https://pydantic.com.cn/usage/validators/)** atau **[root_validator](https://pydantic-docs.helpmanual.io/usage/validators/)** milik Pydantic.

!!! info
    Kunjungi [Ninja Schema](https://pypi.org/project/ninja-schema/) untuk informasi lebih lanjut

## Mengakses Objek Request di dalam Schema
Django Ninja Extra menyediakan objek `RouteContext` yang tersedia selama lifecycle request berlangsung.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
