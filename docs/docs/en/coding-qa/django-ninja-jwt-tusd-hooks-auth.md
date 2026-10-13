---
comments: true
---
Below is a Chinese technical article suitable for a Markdown blog, introducing how to use `django-ninja-jwt` to integrate with `tusd`'s HTTP Hooks for user authentication.

---

# Using django-ninja-jwt to Integrate with tusd's HTTP Hooks for User Authentication

When building large-file upload services that support resumable uploads, [`tusd`](https://github.com/tus/tusd) is a very popular server-side implementation. In Django projects, we typically use the [django-ninja](https://django-ninja.dev) framework together with [django-ninja-jwt](https://pypi.org/project/django-ninja-jwt/) for API development and authentication.

This article will introduce how to combine **tusd's HTTP Hooks** with `django-ninja-jwt` to achieve user identification and upload permission control.

---

## 1. Introduction to tusd's HTTP Hooks

`tusd` supports triggering Hooks at various stages of the upload lifecycle (such as `pre-create`, `post-finish`). You can configure the `--hooks-http` parameter so that `tusd` sends an HTTP request when a Hook is triggered.

Example configuration command:

```bash
tusd \
  -hooks-http http://localhost:8000/tusd-hook/ \
  -cors-allow-origin "http://localhost:8080" \
  -cors-allow-credentials \
  -upload-dir ./uploads
```

When an upload operation occurs, tusd will POST a JSON payload to the specified address, which includes the request headers (such as `Authorization` or `Cookie`) and the upload metadata.

---

## 2. Configuring the JWT Request Header with tus-js-client

When using `tus-js-client` on the frontend (for example, in a Vue/Quasar application), you need to attach the JWT Token in the request header:

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

## 3. Backend: Django Receives the tusd Hook and Verifies the JWT

Create a Hook receiving endpoint in your Django project:

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

## 4. Register the Route

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

## 5. Example of a tusd Hook Request (POST)

tusd will send JSON similar to the following to the backend:

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

## 6. Summary

Through the configuration above, we achieved:

1. The frontend carries the JWT when uploading a file;
2. tusd passes the request headers to the HTTP hook;
3. The backend uses django-ninja-jwt to verify the token and obtain the user;
4. Advanced features such as upload authorization and file ownership binding can be implemented.

---

If you want to add features such as file database records, permission checks, or user quota limits, you can extend the logic on this basis.

tus is truly an upload solution for the new era — resumable uploads are so satisfying. A video demonstration is attached below.
A demonstration of resumable uploads with tus combined with django-ninja-jwt.

<video controls width="600">
  <source src="../img/tus断点续传演示.mov" type="video/quicktime">
  Your browser does not support the video tag.
</video>
