---
comments: true
---
# Paramètres de requête

Lorsque vous déclarez des paramètres de fonction qui ne font pas partie des paramètres de chemin, ils sont automatiquement interprétés comme des paramètres de « requête » (query).
```python hl_lines="5"
{!./src/tutorial/query/code01.py!}
```

Pour interroger cette opération, vous pouvez utiliser une URL comme celle-ci :

```
http://localhost:8000/api/weapons?offset=0&limit=10
```
Par défaut, tous les paramètres GET sont des chaînes ; lorsque vous annotez vos paramètres de fonction avec des types, ils seront convertis vers ce type et validés par rapport à celui-ci.

Les mêmes avantages que pour les paramètres de chemin s'appliquent également aux paramètres de requête :

- Prise en charge par l'éditeur (évidemment)
- « Analyse » des données (parsing)
- Validation des données
- Documentation automatique


!!! note
    Si vous n'annotez pas vos paramètres, ils seront traités comme du type `str`

```python hl_lines="2"
@api.get("/weapons")
def list_weapons(request, limit, offset):
    # type(limit) == str
    # type(offset) == str
```

### Valeurs par défaut

Étant donné que les paramètres de requête ne font pas partie fixe du chemin, ils sont optionnels et peuvent avoir des valeurs par défaut :

```python hl_lines="2"
@api.get("/weapons")
def list_weapons(request, limit: int = 10, offset: int = 0):
    return weapons[offset : offset + limit]
```

Dans l'exemple ci-dessus, nous avons défini les valeurs par défaut de `offset=0` et `limit=10`.

Ainsi, visiter l'URL :
```
http://localhost:8000/api/weapons
```
revient à visiter :
```
http://localhost:8000/api/weapons?offset=0&limit=10
```
Si vous visitez, par exemple :
```
http://localhost:8000/api/weapons?offset=20
```

Les valeurs des paramètres dans votre fonction seront :

 - `offset=20` (parce que vous l'avez défini dans l'URL)
 - `limit=10` (parce que c'est la valeur par défaut)


### Paramètres obligatoires et optionnels

Vous pouvez déclarer des paramètres GET obligatoires ou optionnels de la même manière que vous déclarez des paramètres de fonction Python :

```python hl_lines="5"
{!./src/tutorial/query/code02.py!}
```

Dans ce cas, **Django Ninja** validera toujours le paramètre `q` que vous passez dans la requête GET, tandis que le paramètre `offset` est un entier optionnel.

### Conversion des types des paramètres GET

Déclarons plusieurs paramètres typés :
```python hl_lines="5"
{!./src/tutorial/query/code03.py!}
```
Le type `str` est passé tel quel.

Pour le type `bool`, pour tous les cas suivants :
```
http://localhost:8000/api/example?b=1
http://localhost:8000/api/example?b=True
http://localhost:8000/api/example?b=true
http://localhost:8000/api/example?b=on
http://localhost:8000/api/example?b=yes
```
ou toute autre variation de casse (majuscules, capitalisation, etc.), votre fonction verra
que le paramètre `b` a la valeur `bool` `True`, sinon `False`.

Les dates peuvent être des chaînes de date et des entiers (horodatages Unix) :

<pre style="font-size: .85em; background-color:rgb(245, 245, 245);">
http://localhost:8000/api/example?d=<strong>1577836800</strong>  # equivalent to 2020-01-01
http://localhost:8000/api/example?d=<strong>2020-01-01</strong>
</pre>


### Utilisation d'un Schema

Vous pouvez également utiliser un schéma pour encapsuler les paramètres GET :

```python hl_lines="1 2  5 6 7 8"
{!./src/tutorial/query/code010.py!}
```

Pour des scénarios de filtrage plus complexes, reportez-vous au [Filtrage](./filtering.md).

!!! done

    Poursuivez avec le chapitre suivant ! **[Corps de la requête](body.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
