---
comments: true
---
# Tutoriel - Gérer les paramètres d'entrée

## Passer des paramètres via la chaîne de requête (query string)

Modifions l'opération pour accepter un nom provenant de la chaîne de requête de l'URL. Pour cela, il suffit d'ajouter un argument `name` à notre fonction.

```python
@api.get("/hello")
def hello(request, name):
    return f"Hello {name}"
```

Lorsque nous fournissons l'argument nommé, nous obtenons la réponse attendue (HTTP 200).

<a href="http://localhost:8000/api/hello?name=you"
target="_blank">localhost:8000/api/hello?name=you</a> :

```json
"Hello you"
```

### Valeurs par défaut

Si vous ne fournissez pas le paramètre, une réponse d'erreur HTTP 422 est renvoyée.

*[HTTP 422] : Unprocessable Entity

<a href="http://localhost:8000/api/hello"
target="_blank">localhost:8000/api/hello</a> :

```json
{
  "detail": [
    {
      "loc": ["query", "name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

Nous pouvons spécifier une valeur par défaut pour l'argument `name` au cas où il ne serait pas fourni :

```python hl_lines="2"
@api.get("/hello")
def hello(request, name="world"):
    return f"Hello {name}"
```

## Types d'entrée

**Django Ninja** utilise les [annotations de types](https://docs.python.org/3/library/typing.html) Python standard pour formater les types d'entrée. Si aucun type n'est fourni, une chaîne de caractères est supposée (mais fournir des annotations de types pour tous les arguments est une bonne pratique).

Ajoutons une deuxième opération qui effectue un calcul basique avec des entiers.

```python hl_lines="5-7"
@api.get("/hello")
def hello(request, name: str = "world"):
    return f"Hello {name}"

@api.get("/math")
def math(request, a: int, b: int):
    return {"add": a + b, "multiply": a * b}
```

<a href="http://localhost:8000/api/math?a=2&b=3"
target="_blank">localhost:8000/api/math?a=2&b=3</a> :

```json
{
  "add": 5,
  "multiply": 6
}
```

## Passer des paramètres via les chaînes de chemin (path)

Vous pouvez déclarer des « paramètres » de chemin en utilisant la même syntaxe que les chaînes de format Python.

Tout paramètre trouvé dans la chaîne de chemin sera transmis à votre fonction comme argument, au lieu d'être pris de la chaîne de requête.

```python hl_lines="1"
@api.get("/math/{a}and{b}")
def math(request, a: int, b: int):
    return {"add": a + b, "multiply": a * b}
```

Nous accédons maintenant à l'opération math via <a href="http://localhost:8000/api/math/2and3"
target="_blank">localhost:8000/api/math/2and3</a>.


## Passer des paramètres via le corps de la requête (request body)

Nous allons changer l'opération `hello` pour utiliser une requête HTTP `POST`, et récupérer les paramètres depuis le corps de la requête.

Pour spécifier que les paramètres proviennent du corps de la requête, nous devons déclarer un Schema.

*[Schema] : Une extension d'un « Model » Pydantic

```python hl_lines="1 5-6 8-10"
from ninja import NinjaAPI, Schema

api = NinjaAPI()

class HelloSchema(Schema):
    name: str = "world"

@api.post("/hello")
def hello(request, data: HelloSchema):
    return f"Hello {data.name}"
```

### API auto-documentée

Désormais, accéder à <a href="http://localhost:8000/api/hello" target="_blank">localhost:8000/api/hello</a> produira une réponse d'erreur HTTP 405, car nous devons changer la requête faite à cette URL pour le type POST.

*[HTTP 405] : Method Not Allowed

Un moyen simple de le faire est d'utiliser la documentation Swagger créée automatiquement pour nous, à l'URL par défaut « /docs » (ajoutée à la racine de l'URL de notre API).

1. Rendez-vous sur <a href="http://localhost:8000/api/docs" target="_blank">localhost:8000/api/docs</a> pour voir les opérations que nous avons créées
1. Ouvrez l'opération `/api/hello`
2. Cliquez sur « Try it out »
3. Modifiez le corps de la requête
4. Cliquez sur « Execute »

!!! success

    Poursuivez avec le chapitre suivant **[Gérer les réponses](step3.md)**
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
