
Untuk melakukan pekerjaan pengembangan pada Ninja JWT, buat fork Anda sendiri di Github,
clone secara lokal, buat dan aktifkan virtual environment untuknya, lalu di dalam direktori proyek:

Setelah itu, instal flit

```shell
$(venv) pip install flit
```

Instal library pengembangan dan pre-commit hooks yang digunakan untuk linting dan style kode

```shell
$(venv) make install
```

Untuk menjalankan pengujian:

```shell
$(venv) make test
```

Untuk menjalankan pengujian dengan coverage:

```shell
$(venv) make test-cov
```

!!! success

    Tutorial ini selesai di sini!

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
