---
comments: true
---
# Die Response anpassen

Manchmal möchten Sie eine Response kurz vor der Auslieferung verändern, zum Beispiel um einen Header hinzuzufügen oder ein Cookie zu ändern.

Dazu deklarieren Sie einfach ein Funktionsargument vom Typ `HttpResponse`:

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


## Temporäres Response-Objekt

Dieses Response-Objekt dient als Basis für alle von Django Ninja erzeugten Responses, einschließlich Fehler-Responses.
Wird ein Django-`HttpResponse`-Objekt direkt von einer Operation zurückgegeben, dann wird dieses Objekt *nicht* verwendet.

Offensichtlich enthält dieses Response-Objekt zu diesem Zeitpunkt noch keinen Inhalt, aber es setzt `content_type` (obwohl Sie das vermutlich nicht ändern wollen).

Der `status_code` wird anhand des Rückgabewerts überschrieben (Standard ist 200, bzw. der Statuscode, wenn ein zweiteiliges Tupel zurückgegeben wird).


## Das Basis-Response-Objekt ändern

Sie können dieses temporäre Response-Objekt ändern, indem Sie die Methode `NinjaAPI.create_temporal_response` überschreiben.

```python
    def create_temporal_response(self, request: HttpRequest) -> HttpResponse:
        response = super().create_temporal_response(request)
        # Do your magic here...
        return response
```

!!! done

    Weiter zum nächsten Kapitel! **[Schemata aus Django-Modellen generieren](django-pydantic.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
