---
comments: true
---
# Paramètres de chemin

Vous pouvez déclarer des « paramètres » de chemin en utilisant la même syntaxe que les chaînes formatées de Python (qui, heureusement, correspond également aux <a href="https://swagger.io/docs/specification/describing-parameters/#path-parameters" target="_blank">paramètres de chemin OpenAPI</a>) :

```python hl_lines="1 2"
{!./src/tutorial/path/code01.py!}
```

La valeur du paramètre de chemin `item_id` sera passée à votre fonction comme argument `item_id`.

Ainsi, si vous exécutez cet exemple et rendez-vous sur <a href="http://localhost:8000/api/items/foo" target="_blank">http://localhost:8000/api/items/foo</a>, vous verrez cette réponse :

```JSON
{"item_id":"foo"}
```


### Paramètres de chemin avec types

Vous pouvez déclarer le type d'un paramètre de chemin à l'aide des annotations de type Python standard dans votre fonction :

```python hl_lines="2"
{!./src/tutorial/path/code02.py!}
```

Dans ce cas, `item_id` est déclaré comme un **`int`**. Cela vous apporte la prise en charge de l'éditeur et du linter pour la vérification des erreurs, la complétion de code, etc.

Si vous exécutez ce code dans votre navigateur avec <a href="http://localhost:8000/api/items/3" target="_blank">http://localhost:8000/api/items/3</a>, vous verrez cette réponse :
```JSON
{"item_id":3}
```

!!! tip
    Notez que la valeur que votre fonction reçoit (et renvoie) est **3**, en tant que `int` Python — et non la chaîne `"3"`.
    Ainsi, avec cette simple déclaration de type, **Django Ninja** vous fournit l'« analyse » (parsing) et la validation automatiques de la requête.



### Validation des données

D'un autre côté, si vous visitez <a href="http://localhost:8000/api/items/foo" target="_blank">http://localhost:8000/api/items/foo</a> <small>*(`"foo"` n'est pas un int)*</small> dans votre navigateur, vous verrez une erreur HTTP comme celle-ci :

```JSON hl_lines="8"
{
    "detail": [
        {
            "loc": [
                "path",
                "item_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```


### Convertisseurs de chemin de Django

Vous pouvez utiliser les [convertisseurs de chemin de Django](https://docs.djangoproject.com/en/stable/topics/http/urls/#path-converters)
pour aider à analyser le chemin :

```python hl_lines="1"
@api.get("/items/{int:item_id}")
def read_item(request, item_id):
    return {"item_id": item_id}
```

Dans ce cas, `item_id` sera analysé comme un **`int`**. Si `item_id` n'est pas un `int` valide, l'URL ne correspondra pas.
(Par exemple, si aucune autre route ne correspond, une erreur 404 Not Found sera renvoyée.)

!!! tip
    Notez que puisque **Django Ninja** utilise le type `str` par défaut pour les paramètres non annotés, la valeur que la fonction ci-dessus reçoit (et renvoie) est `"3"`,
    en tant que `str` Python — et non l'entier **3**. Pour recevoir un `int`, déclarez simplement `item_id` avec une annotation de type `int` dans la définition de la fonction comme d'habitude :

    ```python hl_lines="2"
    @api.get("/items/{int:item_id}")
    def read_item(request, item_id:int):
        return {"item_id": item_id}
    ```

#### Paramètres de chemin avec barres obliques

Le convertisseur `path` de Django vous permet de gérer les paramètres de type chemin :

```python hl_lines="1"
@api.get('/dir/{path:value}')
def someview(request, value: str):
    return value
```
Vous pouvez interroger cette opération avec `/dir/some/path/with-slashes`, et votre `value` sera égale à `some/path/with-slashes`

### Paramètres multiples

Vous pouvez passer autant de variables que vous le souhaitez au `chemin` — pensez simplement à utiliser des noms uniques, et n'oubliez pas d'utiliser les mêmes noms dans les arguments de votre fonction.

```python
@api.get("/events/{year}/{month}/{day}")
def events(request, year: int, month: int, day: int):
    return {"date": [year, month, day]}
```


### Utilisation d'un Schema

Vous pouvez également utiliser un schéma pour encapsuler des paramètres de chemin interdépendants (et les valider en tant que groupe) :


```python hl_lines="1 2  5 6 7 8 9 10 11 15"
{!./src/tutorial/path/code010.py!}
```

!!! note
    Notez qu'ici, nous utilisons une indication de source `Path` pour indiquer à **Django Ninja** que ce schéma sera appliqué aux paramètres de chemin.

### Documentation

Maintenant, lorsque vous ouvrez <a href="http://localhost:8000/api/docs" target="_blank">http://localhost:8000/api/docs</a> dans votre navigateur, vous verrez la documentation interactive automatique de l'API.
![Django Ninja Swagger](../../img/tutorial-path-swagger.png)

!!! done

    Poursuivez avec le chapitre suivant ! **[Paramètres de requête](query-params.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
