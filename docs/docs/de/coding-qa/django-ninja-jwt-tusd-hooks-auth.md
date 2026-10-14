---
comments: true
---
Im Folgenden finden Sie einen technischen Artikel, der sich für einen Markdown-Blog eignet und zeigt, wie man `django-ninja-jwt` für die Integration mit den HTTP-Hooks von `tusd` zur Benutzerauthentifizierung verwendet.

---

# django-ninja-jwt zur Integration mit den HTTP-Hooks von tusd für die Benutzerauthentifizierung verwenden

Beim Aufbau von Upload-Diensten für große Dateien mit fortsetzbaren Uploads (Resumable Upload) ist [`tusd`](https://github.com/tus/tusd) eine sehr beliebte serverseitige Implementierung. In Django-Projekten verwenden wir üblicherweise das Framework [django-ninja](https://django-ninja.dev) zusammen mit [django-ninja-jwt](https://pypi.org/project/django-ninja-jwt/) für die API-Entwicklung und Authentifizierung.

Dieser Artikel zeigt, wie man **die HTTP-Hooks von tusd** mit `django-ninja-jwt` kombiniert, um Benutzeridentifikation und Kontrolle der Upload-Berechtigungen zu erreichen.

---

## 1. Einführung in die HTTP-Hooks von tusd

`tusd` unterstützt das Auslösen von Hooks in verschiedenen Phasen des Upload-Lebenszyklus (z. B. `pre-create`, `post-finish`). Sie können den Parameter `--hooks-http` konfigurieren, sodass `tusd` eine HTTP-Anfrage sendet, wenn ein Hook ausgelöst wird.

Beispiel eines Konfigurationsbefehls:

```bash
tusd \
  -hooks-http http://localhost:8000/tusd-hook/ \
  -cors-allow-origin "http://localhost:8080" \
  -cors-allow-credentials \
  -upload-dir ./uploads
```

Wenn ein Upload-Vorgang stattfindet, sendet tusd eine JSON-Nutzlast per POST an die angegebene Adresse; diese enthält die Request-Header (z. B. `Authorization` oder `Cookie`) und die Upload-Metadaten.

---

## 2. Konfigurieren des JWT-Request-Headers mit tus-js-client

Wenn Sie `tus-js-client` im Frontend verwenden (zum Beispiel in einer Vue/Quasar-Anwendung), müssen Sie den JWT-Token im Request-Header mitgeben:

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

## 3. Backend: Django empfängt den tusd-Hook und verifiziert das JWT

Erstellen Sie in Ihrem Django-Projekt einen Endpunkt zum Empfangen des Hooks:

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

## 4. Route registrieren

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

## 5. Beispiel einer tusd-Hook-Anfrage (POST)

tusd sendet eine JSON-Struktur ähnlich der folgenden an das Backend:

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

## 6. Zusammenfassung

Mit der obigen Konfiguration haben wir erreicht:

1. Das Frontend überträgt das JWT beim Hochladen einer Datei;
2. tusd leitet die Request-Header an den HTTP-Hook weiter;
3. Das Backend verifiziert den Token mit django-ninja-jwt und ermittelt den Benutzer;
4. Erweiterte Funktionen wie Upload-Autorisierung und die Verknüpfung von Dateien mit ihrem Besitzer können implementiert werden.

---

Wenn Sie Funktionen wie Datenbankeinträge für Dateien, Berechtigungsprüfungen oder Benutzerkontingente hinzufügen möchten, können Sie die Logik auf dieser Grundlage erweitern.

tus ist wahrlich eine Upload-Lösung für das neue Zeitalter — fortsetzbare Uploads sind einfach erfüllend. Nachfolgend finden Sie eine Videodemonstration.
Eine Demonstration fortsetzbarer Uploads mit tus in Kombination mit django-ninja-jwt.

<video controls width="600">
  <source src="../img/tus断点续传演示.mov" type="video/quicktime">
  Your browser does not support the video tag.
</video>
