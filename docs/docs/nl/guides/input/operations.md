---
comments: true
---
# HTTP Methoden

## Operaties definiëren

Een `operation` kan een van de [HTTP methoden](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods) zijn:

- GET (ophalen)
- POST (versturen)
- PUT (bijwerken)
- DELETE (verwijderen)
- PATCH (gedeeltelijk bijwerken)

**Django Ninja** heeft een decorator voor elke operatie:

```python hl_lines="1 5 9 13 17"
@api.get("/path")
def get_operation(request):
    ...

@api.post("/path")
def post_operation(request):
    ...

@api.put("/path")
def put_operation(request):
    ...

@api.delete("/path")
def delete_operation(request):
    ...

@api.patch("/path")
def patch_operation(request):
    ...
```

Voor informatie over wat je aan deze decorators kunt doorgeven, zie de referentiedocumentatie [Operatieparameters](../../reference/operations-parameters.md).

## Meerdere methoden afhandelen

Als je meerdere methoden voor een bepaald path met één functie wilt afhandelen, kun je de decorator `api_operation` gebruiken:

```python hl_lines="1"
@api.api_operation(["POST", "PATCH"], "/path")
def mixed_operation(request):
    ...
```

Deze functie kan ook worden gebruikt om andere HTTP methoden te implementeren die geen corresponderende **Django Ninja** methode hebben, zoals `HEAD` of `OPTIONS`.

```python hl_lines="1"
@api.api_operation(["HEAD", "OPTIONS"], "/path")
def mixed_operation(request):
    ...
```

!!! done

    Ga verder naar het volgende hoofdstuk! **[Path Parameters](path-params.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
