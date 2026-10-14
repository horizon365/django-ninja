---
comments: true
---
# Formulierdata

**Django Ninja** stelt je ook in staat om `request.POST` data te parsen en te valideren
(dus `application/x-www-form-urlencoded` of `multipart/form-data`).

## Formulierdata als parameters

```python hl_lines="1 4"
from ninja import NinjaAPI, Form

@api.post("/login")
def login(request, username: Form[str], password: Form[str]):
    return {'username': username, 'password': '*****'}
```

Let op het volgende:

1) Je moet de class `Form` importeren uit `ninja`
```python
from ninja import Form
```

2) Gebruik `Form` als standaardwaarde voor de parameter:
```python
username: Form[str]
```

## Een Schema gebruiken

Net als bij [Request Body](body.md#declare-it-as-a-parameter) kun je een schema gebruiken om je parameters te organiseren.

```python hl_lines="12"
{!./src/tutorial/form/code01.py!}
```

## Request Form + Path + Query Parameters

Net als bij [Request Body](body.md#request-body-path-query-parameters) kun je formulierdata combineren met andere parameterbronnen.

Je kunt query parameters **en** path parameters **en** formuliervelden, **enz.** tegelijk declareren.

**Django Ninja** herkent dat functieparameters die overeenkomen met path parameters **uit het path moeten worden genomen**,
terwijl functieparameters die met `Form(...)` zijn gedeclareerd **uit de request formuliervelden moeten worden genomen**, enzovoort.

```python hl_lines="12"
{!./src/tutorial/form/code02.py!}
```
## Lege formuliervelden mappen naar standaardwaarden

Optionele formuliervelden worden vaak verstuurd met lege waarden. Deze waarde wordt geïnterpreteerd als een lege string, dus voor velden zoals `int` of `bool` kan de validatie mislukken.

Zoals beschreven in de Pydantic documentatie kan dit worden opgelost door [generic classes als types](https://pydantic.com.cn/usage/types/#generic-classes-as-types) te gebruiken.

```python hl_lines="15 16 23-25"
{!./src/tutorial/form/code03.py!}
```

!!! done

    Ga verder naar het volgende hoofdstuk! **[Bestandsuploads](file-params.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
