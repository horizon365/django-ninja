---
comments: true
---
Berikut adalah artikel teknis yang cocok untuk sebuah blog Markdown, memperkenalkan cara menggunakan `django-ninja-jwt` untuk berintegrasi dengan HTTP Hooks milik `tusd` untuk autentikasi user.

---

# Menggunakan django-ninja-jwt untuk Berintegrasi dengan HTTP Hooks tusd guna Autentikasi User

Ketika membangun layanan upload file besar yang mendukung resumable upload, [`tusd`](https://github.com/tus/tusd) adalah salah satu implementasi server-side yang sangat populer. Di project Django, kita biasanya menggunakan framework [django-ninja](https://django-ninja.dev) bersama dengan [django-ninja-jwt](https://pypi.org/project/django-ninja-jwt/) untuk pengembangan API dan autentikasi.

Artikel ini akan memperkenalkan cara menggabungkan **HTTP Hooks tusd** dengan `django-ninja-jwt` untuk mencapai identifikasi user dan kontrol izin upload.

---

## 1. Pengenalan HTTP Hooks tusd

`tusd` mendukung pemicuan Hooks pada berbagai tahap siklus hidup upload (seperti `pre-create`, `post-finish`). Anda dapat mengonfigurasi parameter `--hooks-http` agar `tusd` mengirimkan HTTP request ketika sebuah Hook terpicu.

Contoh perintah konfigurasi:

```bash
tusd \
  -hooks-http http://localhost:8000/tusd-hook/ \
  -cors-allow-origin "http://localhost:8080" \
  -cors-allow-credentials \
  -upload-dir ./uploads
```

Ketika operasi upload terjadi, tusd akan POST sebuah payload JSON ke alamat yang ditentukan, yang mencakup request headers (seperti `Authorization` atau `Cookie`) serta metadata upload.

---

## 2. Mengonfigurasi Request Header JWT dengan tus-js-client

Saat menggunakan `tus-js-client` di frontend (misalnya, dalam aplikasi Vue/Quasar), Anda perlu menyertakan JWT Token di request header:

```js
import tus from 'tus-js-client'

const upload = new tus.Upload(file, {
  endpoint: 'http://localhost:1080/files/',
  metadata: {
    filename: file.name,
    filetype: file.type
  },
  headers: {
    Authorization: 'Bearer ' + localStorage.getItem('access_token') // JWT token
  },
  withCredentials: false, // Do not use cookies; use the Authorization header
  onError: (error) => console.error(error),
  onSuccess: () => console.log('Upload succeeded')
})

upload.start()
```

---

## 3. Backend: Django Menerima Hook tusd dan Memverifikasi JWT

Buat endpoint penerima Hook di project Django Anda:

```python
# views.py
from ninja import Router
from ninja_jwt.authentication import JWTAuth
from django.http import JsonResponse
from django.contrib.auth import get_user_model
import json

router = Router()

@router.post("/tusd-hook")
def tusd_hook(request):
    try:
        payload = json.loads(request.body)
        headers = payload.get("HTTPRequest", {}).get("Header", {})
        auth_header = headers.get("Authorization", [""])[0]

        if auth_header.startswith("Bearer "):
            token = auth_header.split("Bearer ")[1]

            # Use django-ninja-jwt's JWTAuth to parse the token
            user = JWTAuth().authenticate(request, token)

            if user is None:
                return JsonResponse({"error": "Invalid token"}, status=401)

            # user is an authenticated Django User instance
            print("Upload user:", user.username)

            # You can perform authorization or write to the database based on user info
            return JsonResponse({"status": "ok"})

        return JsonResponse({"error": "No token"}, status=401)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
```

---

## 4. Mendaftarkan Route

```python
# urls.py
from django.urls import path
from ninja import NinjaAPI
from .views import router as tusd_router

api = NinjaAPI()
api.add_router("/", tusd_router)

urlpatterns = [
    path("tusd-hook/", api.urls),
]
```

---

## 5. Contoh Request Hook tusd (POST)

tusd akan mengirimkan JSON yang serupa dengan berikut ini ke backend:

```json
{
  "Protocol": "http",
  "EventName": "pre-create",
  "Upload": {
    "ID": "123456",
    "Size": 1024000,
    "MetaData": {
      "filename": "example.pdf",
      "filetype": "application/pdf"
    }
  },
  "HTTPRequest": {
    "Method": "POST",
    "URI": "/files/",
    "Header": {
      "Authorization": ["Bearer <jwt-token>"]
    }
  }
}
```

---

## 6. Ringkasan

Melalui konfigurasi di atas, kita telah mencapai:

1. Frontend menyertakan JWT saat meng-upload file;
2. tusd meneruskan request headers ke HTTP hook;
3. Backend menggunakan django-ninja-jwt untuk memverifikasi token dan mendapatkan user;
4. Fitur-fitur lanjutan seperti otorisasi upload dan pengikatan kepemilikan file dapat diimplementasikan.

---

Jika Anda ingin menambahkan fitur seperti pencatatan file di database, pemeriksaan izin, atau pembatasan kuota user, Anda dapat mengembangkan logikanya di atas dasar ini.

tus benar-benar merupakan solusi upload untuk era baru — resumable upload memuaskan sekali. Berikut dilampirkan video demonstrasi.
Sebuah demonstrasi resumable upload dengan tus yang dikombinasikan dengan django-ninja-jwt.

<video controls width="600">
  <source src="../img/tus断点续传演示.mov" type="video/quicktime">
  Your browser does not support the video tag.
</video>
