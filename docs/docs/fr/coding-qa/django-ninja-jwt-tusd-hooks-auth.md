---
comments: true
---
Voici un article technique en chinois, adapté à un blog Markdown, qui présente comment utiliser `django-ninja-jwt` pour s'intégrer avec les HTTP Hooks de `tusd` pour l'authentification des utilisateurs.

---

# Utiliser django-ninja-jwt pour s'intégrer avec les HTTP Hooks de tusd pour l'authentification des utilisateurs

Lors de la construction de services d'upload de gros fichiers prenant en charge les uploads reprenables, [`tusd`](https://github.com/tus/tusd) est une implémentation côté serveur très populaire. Dans les projets Django, nous utilisons généralement le framework [django-ninja](https://django-ninja.dev) avec [django-ninja-jwt](https://pypi.org/project/django-ninja-jwt/) pour le développement d'API et l'authentification.

Cet article présentera comment combiner **les HTTP Hooks de tusd** avec `django-ninja-jwt` pour réaliser l'identification des utilisateurs et le contrôle des permissions d'upload.

---

## 1. Introduction aux HTTP Hooks de tusd

`tusd` prend en charge le déclenchement de Hooks à différentes étapes du cycle de vie de l'upload (comme `pre-create`, `post-finish`). Vous pouvez configurer le paramètre `--hooks-http` pour que `tusd` envoie une requête HTTP lorsqu'un Hook est déclenché.

Exemple de commande de configuration :

```bash
tusd \
  -hooks-http http://localhost:8000/tusd-hook/ \
  -cors-allow-origin "http://localhost:8080" \
  -cors-allow-credentials \
  -upload-dir ./uploads
```

Lorsqu'une opération d'upload se produit, tusd enverra en POST une charge utile JSON à l'adresse spécifiée, qui inclut les en-têtes de la requête (comme `Authorization` ou `Cookie`) et les métadonnées de l'upload.

---

## 2. Configuration de l'en-tête de requête JWT avec tus-js-client

Lors de l'utilisation de `tus-js-client` côté frontend (par exemple, dans une application Vue/Quasar), vous devez joindre le jeton JWT dans l'en-tête de la requête :

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

## 3. Backend : Django reçoit le Hook de tusd et vérifie le JWT

Créez un endpoint de réception de Hook dans votre projet Django :

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

## 4. Enregistrement de la route

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

## 5. Exemple d'une requête de Hook tusd (POST)

tusd enverra au backend un JSON similaire à ce qui suit :

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

## 6. Résumé

Grâce à la configuration ci-dessus, nous avons réalisé :

1. Le frontend transporte le JWT lors de l'upload d'un fichier ;
2. tusd transmet les en-têtes de la requête au hook HTTP ;
3. Le backend utilise django-ninja-jwt pour vérifier le jeton et obtenir l'utilisateur ;
4. Des fonctionnalités avancées telles que l'autorisation d'upload et la liaison de la propriété des fichiers peuvent être mises en œuvre.

---

Si vous souhaitez ajouter des fonctionnalités telles que des enregistrements de fichiers en base de données, des vérifications de permissions ou des limites de quota utilisateur, vous pouvez étendre la logique sur cette base.

tus est vraiment une solution d'upload pour la nouvelle ère — les uploads reprenables, quelle satisfaction. Une démonstration vidéo est jointe ci-dessous.
Une démonstration d'upload reprenable avec tus combiné à django-ninja-jwt.

<video controls width="600">
  <source src="../img/tus断点续传演示.mov" type="video/quicktime">
  Your browser does not support the video tag.
</video>
