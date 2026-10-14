---
comments: true
---
# Méthodes HTTP

## Définition des opérations

Une `opération` peut correspondre à l'une des [méthodes HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods) :

- GET (récupérer)
- POST (soumettre)
- PUT (mettre à jour)
- DELETE (supprimer)
- PATCH (mise à jour partielle)

**Django Ninja** possède un décorateur pour chaque opération :

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

Pour savoir ce qui peut être passé à l'un de ces décorateurs, consultez la documentation de référence sur les [Paramètres d'opération](../../reference/operations-parameters.md).

## Gestion de plusieurs méthodes

Si vous devez gérer plusieurs méthodes pour un chemin donné avec une seule fonction, vous pouvez utiliser le décorateur `api_operation` :

```python hl_lines="1"
@api.api_operation(["POST", "PATCH"], "/path")
def mixed_operation(request):
    ...
```

Cette fonctionnalité peut également être utilisée pour implémenter d'autres méthodes HTTP qui n'ont pas de méthode **Django Ninja** correspondante, comme `HEAD` ou `OPTIONS`.

```python hl_lines="1"
@api.api_operation(["HEAD", "OPTIONS"], "/path")
def mixed_operation(request):
    ...
```

!!! done

    Poursuivez avec le chapitre suivant ! **[Paramètres de chemin](path-params.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
