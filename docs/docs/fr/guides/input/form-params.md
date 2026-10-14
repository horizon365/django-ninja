---
comments: true
---
# Données de formulaire

**Django Ninja** vous permet également d'analyser et de valider les données `request.POST`
(c'est-à-dire `application/x-www-form-urlencoded` ou `multipart/form-data`).

## Données de formulaire en tant que paramètres

```python hl_lines="1 4"
from ninja import NinjaAPI, Form

@api.post("/login")
def login(request, username: Form[str], password: Form[str]):
    return {'username': username, 'password': '*****'}
```

Notez ce qui suit :

1) Vous devez importer la classe `Form` depuis `ninja`
```python
from ninja import Form
```

2) Utilisez `Form` comme valeur par défaut du paramètre :
```python
username: Form[str]
```

## Utilisation d'un Schema

Semblable au [Corps de la requête](body.md#declare-it-as-a-parameter), vous pouvez utiliser un schéma pour organiser vos paramètres.

```python hl_lines="12"
{!./src/tutorial/form/code01.py!}
```

## Formulaire de requête + Chemin + Paramètres de requête

Semblable au [Corps de la requête](body.md#request-body-path-query-parameters), vous pouvez combiner les données de formulaire avec d'autres sources de paramètres.

Vous pouvez déclarer en même temps des paramètres de requête **et** des paramètres de chemin **et** des champs de formulaire, **etc.**

**Django Ninja** reconnaîtra que les paramètres de fonction correspondant aux paramètres de chemin doivent être **pris du chemin**,
tandis que les paramètres de fonction déclarés avec `Form(...)` doivent être **pris des champs de formulaire de la requête**, et ainsi de suite.

```python hl_lines="12"
{!./src/tutorial/form/code02.py!}
```
## Correspondance des champs de formulaire vides avec des valeurs par défaut

Les champs de formulaire optionnels sont souvent envoyés avec des valeurs vides. Cette valeur est interprétée comme une chaîne vide, donc pour des champs tels que `int` ou `bool`, la validation peut échouer.

Comme décrit dans la documentation de Pydantic, cela peut être résolu en utilisant [des classes génériques comme types](https://pydantic.com.cn/usage/types/#generic-classes-as-types).

```python hl_lines="15 16 23-25"
{!./src/tutorial/form/code03.py!}
```

!!! done

    Poursuivez avec le chapitre suivant ! **[Téléversement de fichiers](file-params.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
