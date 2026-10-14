---
comments: true
---
# HTTP-Methoden

## Operationen definieren

Eine `operation` kann eine der [HTTP-Methoden](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods) sein:

- GET (abrufen)
- POST (übermitteln)
- PUT (aktualisieren)
- DELETE (löschen)
- PATCH (teilweise aktualisieren)

**Django Ninja** stellt für jede Operation einen Dekorator bereit:

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

Informationen dazu, was an einen dieser Dekoratoren übergeben werden kann, finden Sie in der Referenzdokumentation [Operation-Parameter](../../reference/operations-parameters.md).

## Mehrere Methoden verarbeiten

Wenn Sie mehrere Methoden für einen bestimmten Pfad mit einer einzigen Funktion verarbeiten müssen, können Sie den Dekorator `api_operation` verwenden:

```python hl_lines="1"
@api.api_operation(["POST", "PATCH"], "/path")
def mixed_operation(request):
    ...
```

Diese Funktion lässt sich auch dazu verwenden, andere HTTP-Methoden zu implementieren, für die es keine entsprechende **Django-Ninja**-Methode gibt, wie zum Beispiel `HEAD` oder `OPTIONS`.

```python hl_lines="1"
@api.api_operation(["HEAD", "OPTIONS"], "/path")
def mixed_operation(request):
    ...
```

!!! done

    Weiter zum nächsten Kapitel! **[Path-Parameter](path-params.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
