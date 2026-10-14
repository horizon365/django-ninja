Cara Export File Schema dengan `export_openapi_schema` Setelah Mengkustomisasi Path API Tingkat Atas
==========================================================
Route tingkat atas bawaan di ninja adalah `'api'`. Misalnya Anda mengubahnya menjadi `'coast/api'` lalu menjalankan
`python manage.py export_openapi_schema`, maka akan muncul error.

```python
python manage.py export_openapi_schema 
System check identified some issues:

WARNINGS:
?: (ckeditor.W001) django-ckeditor bundles CKEditor 4.22.1 which isn't supported anmyore and which does have unfixed security issues, see for example https://ckeditor.com/cke4/release/CKEditor-4.24.0-LTS . You should consider strongly switching to a different editor (maybe CKEditor 5 respectively django-ckeditor-5 after checking whether the CKEditor 5 license terms work for you) or switch to the non-free CKEditor 4 LTS package. See https://ckeditor.com/ckeditor-4-support/ for more on this. (Note! This notice has been added by the django-ckeditor developers and we are not affiliated with CKSource and were not involved in the licensing change, so please refrain from complaining to us. Thanks.)
Traceback (most recent call last):
  File "/Users/baoge/WebstormProjects/coast_be/manage.py", line 27, in <module>
    main()
  File "/Users/baoge/WebstormProjects/coast_be/manage.py", line 23, in main
    execute_from_command_line(sys.argv)
  File "/opt/anaconda3/envs/coast_be/lib/python3.10/site-packages/django/core/management/__init__.py", line 419, in execute_from_command_line
    utility.execute()
  File "/opt/anaconda3/envs/coast_be/lib/python3.10/site-packages/django/core/management/__init__.py", line 413, in execute
    self.fetch_command(subcommand).run_from_argv(self.argv)
  File "/opt/anaconda3/envs/coast_be/lib/python3.10/site-packages/django/core/management/base.py", line 354, in run_from_argv
    self.execute(*args, **cmd_options)
  File "/opt/anaconda3/envs/coast_be/lib/python3.10/site-packages/django/core/management/base.py", line 398, in execute
    output = self.handle(*args, **options)
  File "/opt/anaconda3/envs/coast_be/lib/python3.10/site-packages/ninja/management/commands/export_openapi_schema.py", line 79, in handle
    api = self._get_api_instance(options["api"])
  File "/opt/anaconda3/envs/coast_be/lib/python3.10/site-packages/ninja/management/commands/export_openapi_schema.py", line 34, in _get_api_instance
    return resolve("/api/").func.keywords["api"]  # type: ignore
  File "/opt/anaconda3/envs/coast_be/lib/python3.10/site-packages/django/urls/base.py", line 24, in resolve
    return get_resolver(urlconf).resolve(path)
  File "/opt/anaconda3/envs/coast_be/lib/python3.10/site-packages/django/urls/resolvers.py", line 589, in resolve
    raise Resolver404({'tried': tried, 'path': new_path})
django.urls.exceptions.Resolver404: {'tried': [[<URLResolver <URLResolver list> (None:None) 'coast/'>]], 'path': 'api/'}
```
Hal ini terjadi karena source code secara default menggunakan `api = resolve("/api/").func.keywords["api"]`.
Jika route tingkat atas Anda bukan `/api/`, Anda harus menentukannya melalui parameter `--api`. Parameter ini dimuat melalui `import_string(api_path)`, sehingga harus berupa import path dari instance `NinjaAPI`.
Sebagai contoh, di project saya nilainya adalah `'website.utils.tools.api.ninja_api'`. Jika Anda tidak menemukannya, cek di `urls.py` variabel yang berada di depan `add_router` atau `urls` — itulah yang Anda butuhkan.

Pengetahuan tambahan:

## Me
Pada kode ini, jika parameter `--api` diberikan melalui command line, seperti apa formatnya?



## AI Assistant
Pada kode ini, parameter `--api` digunakan untuk menentukan modul instance API. Sesuai dengan komentar dan docstring dalam kode tersebut, format parameter `--api` seharusnya adalah **module path** — tepatnya, sebuah Python module path yang dapat di-resolve oleh fungsi `import_string` milik Django.

### Format
```shell script
--api <module_path>
```


### Contoh
Misalkan struktur project Anda adalah sebagai berikut:
```
project/
    urls.py
    api.py
```


Jika instance `NinjaAPI` didefinisikan di file `project/api.py` dan instance tersebut bernama `api`, Anda dapat memberikan parameter seperti ini:
```shell script
python manage.py export_openapi_schema --api project.api.api
```


### Catatan
1. `<module_path>` adalah Python module path yang menunjuk ke modul yang berisi instance `NinjaAPI`.
2. Bagian terakhir dari path adalah nama variabel dari instance `NinjaAPI` di dalam modul tersebut (misalnya, `api`).
3. Jika parameter `--api` tidak diberikan, kode akan mencoba mengambil instance `NinjaAPI` secara dinamis melalui `resolve("/api/")`. Jika gagal, akan muncul error yang meminta pengguna untuk menentukannya secara eksplisit melalui parameter `--api`.



#### Metode 1: Periksa konfigurasi URL project
Biasanya, URL route untuk sebuah project Django dikonfigurasi di file `urls.py`. Buka `urls.py` project Anda dan cari bagian yang terkait dengan `/api/`. Misalnya:

```python
# project/urls.py
from django.urls import path
from .api import api  # Assume the NinjaAPI instance is named `api`

urlpatterns = [
    path("coast/api/", api.urls),  # Mount `api`'s routes under `/coast/api/`
]
```


Pada contoh ini:
- `api` adalah instance `NinjaAPI`.
- Instance tersebut didefinisikan di modul `project.api` (dengan asumsi direktori root project adalah `project`).

Oleh karena itu, parameter `--api` yang setara adalah:
```shell script
--api project.api.api
```


### Ringkasan
Untuk mereplikasi perilaku `resolve("/coast/api/")`, Anda perlu mengetahui module path dari instance `NinjaAPI` yang dipetakan oleh path `/coast/api/`, lalu memberikannya sebagai nilai parameter `--api`. Misalnya:

```shell script
python manage.py export_openapi_schema --api project.api.api
```


Jika Anda tidak yakin di mana lokasi instance tersebut, periksa file `urls.py` project Anda atau konfirmasikan melalui debugging.
