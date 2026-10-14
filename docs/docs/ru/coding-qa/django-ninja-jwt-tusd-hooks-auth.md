---
comments: true
---
Ниже представлена техническая статья на китайском языке, подходящая для блога в формате Markdown, в которой рассказывается, как использовать `django-ninja-jwt` для интеграции с HTTP Hooks сервиса `tusd` с целью аутентификации пользователей.

---

# Использование django-ninja-jwt для интеграции с HTTP Hooks сервиса tusd с целью аутентификации пользователей

При создании сервиса загрузки больших файлов с поддержкой возобновляемой загрузки [`tusd`](https://github.com/tus/tusd) является очень популярной серверной реализацией. В проектах Django для разработки API и аутентификации мы обычно используем фреймворк [django-ninja](https://django-ninja.dev) вместе с [django-ninja-jwt](https://pypi.org/project/django-ninja-jwt/).

В этой статье будет рассказано, как объединить **HTTP Hooks сервиса tusd** с `django-ninja-jwt` для достижения идентификации пользователей и управления правами на загрузку.

---

## 1. Знакомство с HTTP Hooks сервиса tusd

`tusd` поддерживает срабатывание Hooks на различных этапах жизненного цикла загрузки (например, `pre-create`, `post-finish`). Вы можете настроить параметр `--hooks-http` так, чтобы `tusd` отправлял HTTP-запрос при срабатывании Hook.

Пример команды конфигурации:

```bash
tusd \
  -hooks-http http://localhost:8000/tusd-hook/ \
  -cors-allow-origin "http://localhost:8080" \
  -cors-allow-credentials \
  -upload-dir ./uploads
```

При выполнении операции загрузки tusd отправит POST-запрос с JSON-полезной нагрузкой на указанный адрес, где будут содержаться заголовки запроса (например, `Authorization` или `Cookie`) и метаданные загрузки.

---

## 2. Настройка заголовка JWT-запроса с помощью tus-js-client

При использовании `tus-js-client` на frontend (например, в приложении Vue/Quasar) необходимо прикреплять JWT-токен в заголовке запроса:

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

## 3. Backend: Django принимает Hook от tusd и проверяет JWT

Создайте эндпоинт приёма Hook в вашем проекте Django:

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

## 4. Регистрация маршрута

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

## 5. Пример Hook-запроса от tusd (POST)

tusd отправит на backend JSON, похожий на следующий:

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

## 6. Итог

Благодаря описанной выше конфигурации мы достигли следующего:

1. frontend передаёт JWT при загрузке файла;
2. tusd передаёт заголовки запроса в HTTP hook;
3. backend использует django-ninja-jwt для проверки токена и получения пользователя;
4. можно реализовать расширенные возможности, такие как авторизация загрузки и привязка прав владения файлом.

---

Если вы хотите добавить такие возможности, как записи файлов в базе данных, проверки прав доступа или ограничения квот пользователей, вы можете расширить логику на этой основе.

tus — это по-настоящему решение для загрузки файлов новой эпохи — возобновляемая загрузка настолько удовлетворительна. Ниже прилагается видео-демонстрация.
Демонстрация возобновляемой загрузки с tus в сочетании с django-ninja-jwt.

<video controls width="600">
  <source src="../img/tus断点续传演示.mov" type="video/quicktime">
  Your browser does not support the video tag.
</video>
