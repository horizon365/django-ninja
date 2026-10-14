---
comments: true
---
Hieronder volgt een Chinees technisch artikel, geschikt voor een Markdown-blog, dat introduceert hoe je `django-ninja-jwt` kunt gebruiken om aan te sluiten op de HTTP Hooks van `tusd` voor gebruikersauthenticatie.

---

# django-ninja-jwt gebruiken om aan te sluiten op de HTTP Hooks van tusd voor gebruikersauthenticatie

Bij het bouwen van uploadservices voor grote bestanden die hervatbare uploads ondersteunen, is [`tusd`](https://github.com/tus/tusd) een zeer populaire serverimplementatie. In Django-projecten gebruiken we doorgaans het [django-ninja](https://django-ninja.dev)-framework samen met [django-ninja-jwt](https://pypi.org/project/django-ninja-jwt/) voor API-ontwikkeling en authenticatie.

Dit artikel introduceert hoe je **de HTTP Hooks van tusd** combineert met `django-ninja-jwt` om gebruikersidentificatie en controle van uploadmachtigingen te realiseren.

---

## 1. Introductie tot de HTTP Hooks van tusd

`tusd` ondersteunt het activeren van Hooks in verschillende fasen van de uploadlevenscyclus (zoals `pre-create`, `post-finish`). Je kunt de parameter `--hooks-http` configureren zodat `tusd` een HTTP-request verstuurt zodra een Hook wordt geactiveerd.

Voorbeeld van een configuratiecommando:

```bash
tusd \
  -hooks-http http://localhost:8000/tusd-hook/ \
  -cors-allow-origin "http://localhost:8080" \
  -cors-allow-credentials \
  -upload-dir ./uploads
```

Wanneer een uploadbewerking plaatsvindt, stuurt tusd een JSON-payload als POST naar het opgegeven adres, inclusief de request headers (zoals `Authorization` of `Cookie`) en de uploadmetadata.

---

## 2. De JWT-requestheader configureren met tus-js-client

Wanneer je `tus-js-client` aan de frontend gebruikt (bijvoorbeeld in een Vue/Quasar-applicatie), moet je het JWT-token in de requestheader meesturen:

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

## 3. Backend: Django ontvangt de tusd Hook en verifieert de JWT

Maak een hook-ontvangstendpoint in je Django-project:

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

## 4. De route registreren

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

## 5. Voorbeeld van een tusd Hook-request (POST)

tusd stuurt JSON die lijkt op het volgende naar de backend:

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

## 6. Samenvatting

Met de bovenstaande configuratie hebben we bereikt:

1. De frontend stuurt de JWT mee bij het uploaden van een bestand;
2. tusd geeft de request headers door aan de HTTP hook;
3. De backend gebruikt django-ninja-jwt om het token te verifiëren en de gebruiker op te halen;
4. Geavanceerde functies zoals uploadautorisatie en koppeling van bestandseigendom kunnen worden geïmplementeerd.

---

Als je functies wilt toevoegen zoals bestandsregistratie in de database, machtigingscontroles of quotumlimieten per gebruiker, kun je de logica op deze basis uitbreiden.

tus is echt een uploadoplossing voor het nieuwe tijdperk — hervatbare uploads zijn zo bevredigend. Hieronder een videodemonstratie.
Een demonstratie van hervatbare uploads met tus in combinatie met django-ninja-jwt.

<video controls width="600">
  <source src="../img/tus断点续传演示.mov" type="video/quicktime">
  Je browser ondersteunt de video-tag niet.
</video>
