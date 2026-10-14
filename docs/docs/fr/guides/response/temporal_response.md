---
comments: true
---
# Ajustement de la réponse

Parfois, vous voudrez modifier une réponse juste avant qu'elle ne soit servie, par exemple pour ajouter un en-tête ou modifier un cookie.

Pour ce faire, déclarez simplement un argument de fonction de type `HttpResponse` :

```python
from django.http import HttpRequest, HttpResponse

@api.get("/cookie/")
def feed_cookiemonster(request: HttpRequest, response: HttpResponse):
    # Set a cookie.
    response.set_cookie("cookie", "delicious")
    # Set a header.
    response["X-Cookiemonster"] = "blue"
    return {"cookiemonster_happy": True}
```


## Objet de réponse temporaire

Cet objet de réponse sert de base à toutes les réponses construites par Django Ninja, y compris les réponses d'erreur.
Si un objet `HttpResponse` de Django est renvoyé directement par une opération, alors cet objet n'est *pas* utilisé.

Évidemment, cet objet de réponse ne contiendra pas encore de contenu, mais il définit bien `content_type` (bien que vous ne souhaitiez probablement pas le modifier).

Le `status_code` sera redéfini en fonction de la valeur de retour (par défaut 200, ou le code de statut si un tuple à deux éléments est renvoyé).


## Modification de l'objet de réponse de base

Vous pouvez modifier cet objet de réponse temporaire en redéfinissant la méthode `NinjaAPI.create_temporal_response`.

```python
    def create_temporal_response(self, request: HttpRequest) -> HttpResponse:
        response = super().create_temporal_response(request)
        # Do your magic here...
        return response
```

!!! done

    Poursuivez avec le chapitre suivant ! **[Génération de Schemas à partir des models Django](django-pydantic.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
