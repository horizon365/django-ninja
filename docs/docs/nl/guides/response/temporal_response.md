---
comments: true
---
# De Response Aanpassen

Soms wil je een response net aanpassen voordat deze wordt aangeleverd, bijvoorbeeld om een header toe te voegen of een cookie te wijzigen.

Hiervoor declareer je simpelweg een functieargument van het type `HttpResponse`:

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


## Tijdelijk Response Object

Dit response object wordt gebruikt als basis voor alle responses die door Django Ninja worden gebouwd, inclusief fout responses.
Als een Django `HttpResponse` object rechtstreeks door een operatie wordt teruggegeven, dan wordt dit object *niet* gebruikt.

Uiteraard bevat dit response object nog geen content, maar het stelt wel `content_type` in (hoewel je die waarschijnlijk niet wilt wijzigen).

De `status_code` wordt overschreven op basis van de retourwaarde (standaard is dit 200, of de statuscode wanneer er een tuple van twee elementen wordt teruggegeven).


## Het Basis Response Object Wijzigen

Je kunt dit tijdelijke response object wijzigen door de methode `NinjaAPI.create_temporal_response` te overriden.

```python
    def create_temporal_response(self, request: HttpRequest) -> HttpResponse:
        response = super().create_temporal_response(request)
        # Do your magic here...
        return response
```

!!! done

    Ga verder naar het volgende hoofdstuk! **[Schemas Genereren vanuit Django Models](django-pydantic.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
