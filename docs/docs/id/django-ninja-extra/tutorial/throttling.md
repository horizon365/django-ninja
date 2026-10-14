---
comments: true
---
# **Throttling / Kontrol Laju**

Throttling dapat dianggap sebagai permission yang menentukan apakah sebuah request harus diizinkan atau tidak.
Throttling merepresentasikan status sementara yang digunakan untuk mengontrol laju di mana client dapat membuat request ke API.

```python
from ninja_extra import NinjaExtraAPI, throttle
api = NinjaExtraAPI()

@api.get('/users')
@throttle  # This will apply the default throttle classes [UserRateThrottle, AnonRateThrottle]
def my_throttled_endpoint(request):
    return 'foo'
```

!!! note
    Contoh di atas tidak akan di-throttle, karena scope default dari `UserRateThrottle` dan `AnonRateThrottle` adalah `none`

## **Throttling Berganda**
Throttling pada django-ninja-extra mendukung beberapa throttle sekaligus, yang berguna untuk menerapkan batasan berbeda pada sebuah API,
seperti throttle rate burst atau throttle rate sustain.
Sebagai contoh, Anda mungkin ingin membatasi user maksimal 60 request per menit dan 1000 request per hari.

```python
from ninja_extra import NinjaExtraAPI, throttle
from ninja_extra.throttling import UserRateThrottle
api = NinjaExtraAPI()

class User60MinRateThrottle(UserRateThrottle):
    rate = "60/min"
    scope = "minutes"


class User1000PerDayRateThrottle(UserRateThrottle):
    rate = "1000/day"
    scope = "days"

@api.get('/users')
@throttle(User60MinRateThrottle, User1000PerDayRateThrottle)
def my_throttled_endpoint(request):
    return 'foo'

```
## **Pengaturan Kebijakan Throttle**
Anda dapat mengatur kelas dan rate throttle default secara global di `settings.py` proyek Anda dengan meng-override key berikut:
```python
# django settings.py
NINJA_EXTRA = {
    'THROTTLE_CLASSES': [
        "ninja_extra.throttling.AnonRateThrottle",
        "ninja_extra.throttling.UserRateThrottle",
    ],
    'THROTTLE_RATES': {
        'user': '1000/day',
        'anon': '100/day',
    },
    'NUM_PROXIES': None
}
```
Deskripsi rate yang digunakan dalam `THROTTLE_RATES` dapat mencakup `second`, `minute`, `hour`, atau `day` sebagai periode throttle.

```python
from ninja_extra import NinjaExtraAPI, throttle
from ninja_extra.throttling import UserRateThrottle

api = NinjaExtraAPI()

@api.get('/users')
@throttle(UserRateThrottle)
def my_throttled_endpoint(request):
    return 'foo'
```

## **Identifikasi Client**
Client diidentifikasi melalui HTTP header X-Forwarded-For dan variabel WSGI REMOTE_ADDR.
Keduanya adalah identifier unik yang digunakan untuk mengidentifikasi alamat IP client untuk throttling.
`X-Forwarded-For` diutamakan daripada `REMOTE_ADDR` dan digunakan sebagai demikian.

#### **Membatasi Proxy Client**
Jika Anda perlu mengidentifikasi alamat IP client yang unik secara ketat, Anda pertama-tama perlu mengonfigurasi jumlah application proxy yang berjalan di belakang API dengan mengatur setting `NUM_PROXIES`. Setting ini harus berupa bilangan bulat nol atau lebih.
Jika diatur dengan nilai bukan nol, maka setelah alamat IP application proxy dikecualikan terlebih dahulu, IP client akan diidentifikasi sebagai alamat IP terakhir pada header X-Forwarded-For. Jika diatur nol, nilai REMOTE_ADDR akan selalu digunakan sebagai alamat IP yang mengidentifikasi.
Penting untuk dipahami bahwa jika Anda mengonfigurasi `NUM_PROXIES`, maka semua client di belakang satu gateway [Network Address Translation (NAT)](https://en.wikipedia.org/wiki/Network_address_translation) yang unik akan diperlakukan sebagai satu client.

!!! note
    Konteks lebih lanjut tentang cara kerja header X-Forwarded-For dan tentang identifikasi IP client remote dapat dibaca di sini.

## **Pengaturan Cache Model Throttle**
Model throttle yang digunakan dalam django-ninja-extra memanfaatkan cache backend Django. Cache menggunakan nilai `default` dari [`LocMemCache`]().
Untuk detail lebih lanjut, silakan merujuk ke [dokumentasi cache](https://docs.djangoproject.com/en/stable/topics/cache/#setting-up-the-cache) Django.

Jika Anda tidak ingin menggunakan cache default yang didefinisikan pada model throttle, berikut adalah contoh cara mendefinisikan cache yang berbeda untuk model throttle:
```python

from django.core.cache import caches
from ninja_extra.throttling import AnonRateThrottle


class CustomAnonRateThrottle(AnonRateThrottle):
    cache = caches['alternate']
```
## **Referensi API**

## **Throttling Rate Anonim**
Model `AnonRateThrottle` digunakan untuk pembatasan throttle dengan menggunakan alamat IP user yang tidak terautentikasi sebagai key.

Model ini cocok untuk membatasi laju request dari sumber yang tidak diketahui.

Permission request ditentukan oleh:
- `rate` yang didefinisikan pada kelas turunannya
- scope `anon` yang didefinisikan pada `THROTTLE_RATES` di pengaturan `NINJA_EXTRA` pada `settings.py`.

## **Throttling Rate User**
Model `UserRateThrottle` digunakan untuk pembatasan throttle dengan menghasilkan key menggunakan user ID atau primary key dari user yang terautentikasi.
Request yang tidak terautentikasi akan kembali menggunakan alamat IP dari request yang masuk untuk menghasilkan key unik untuk pembatasan throttle.

Permission request ditentukan oleh:
- `rate` yang didefinisikan pada kelas turunannya
- scope `user` yang didefinisikan pada `THROTTLE_RATES` di pengaturan `NINJA_EXTRA` pada `settings.py`.


Anda dapat menggunakan beberapa user throttle rate untuk model `UserRateThrottle`, misalnya:
```python
# example/throttles.py
from ninja_extra.throttling import UserRateThrottle


class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'


class SustainedRateThrottle(UserRateThrottle):
    scope = 'sustained'
```

```python
# django settings.py
NINJA_EXTRA = {
    'THROTTLE_CLASSES': [
        'example.throttles.BurstRateThrottle',
        'example.throttles.SustainedRateThrottle'
    ],
    'THROTTLE_RATES': {
        'burst': '60/min',
        'sustained': '1000/day'
    }
}
```
## **Throttling Rate Dinamis**
Model `DynamicRateThrottle` digunakan untuk melakukan throttle terhadap user yang terautentikasi maupun yang tidak terautentikasi dengan cara serupa seperti `UserRateThrottle`.
Fitur utamanya adalah kemampuan untuk mengatur `scope` secara dinamis saat digunakan.
Sebagai contoh:
Kita dapat mendefinisikan scope di pengaturan.

```python
# django settings.py
NINJA_EXTRA = {
    'THROTTLE_RATES': {
        'burst': '60/min',
        'sustained': '1000/day'
    }
}
```

```python
# api.py
from ninja_extra import NinjaExtraAPI, throttle
from ninja_extra.throttling import DynamicRateThrottle
api = NinjaExtraAPI()

@api.get('/users')
@throttle(DynamicRateThrottle, scope='burst')
def get_users(request):
    return 'foo'

@api.get('/users/<int:id>')
@throttle(DynamicRateThrottle, scope='sustained')
def get_user_by_id(request, id: int):
    return 'foo'
```
Di sini, kita menerapkan rate `sustained` dan rate `burst` secara dinamis ke `get_users` dan `get_user_by_id` masing-masing.


!!! note "Baru di v0.15.8"
    Anda dapat melakukan throttle pada semua operasi endpoint controller di tingkat kelas controller.

## **Throttling Controller**

```python
# api.py
from ninja_extra import (
    NinjaExtraAPI, throttle, api_controller, ControllerBase,
    http_get
)
from ninja_extra.throttling import DynamicRateThrottle
api = NinjaExtraAPI()

@api_controller("/throttled-controller")
class ThrottlingControllerSample(ControllerBase):
    throttling_classes = [
        DynamicRateThrottle,
    ]
    throttling_init_kwargs = dict(scope="sustained")

    @http_get("/endpoint_1")
    @throttle(DynamicRateThrottle, scope='burst')
    def endpoint_1(self, request):
        # this will override the generally throttling applied at the controller
        return "foo"

    @http_get("/endpoint_2")
    def endpoint_2(self, request):
        return "foo"

    @http_get("/endpoint_3")
    def endpoint_3(self, request):
        return "foo"


api.register_controllers(ThrottlingControllerSample)
```
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
