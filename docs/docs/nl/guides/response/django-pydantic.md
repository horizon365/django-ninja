---
comments: true
---
# Schemas Genereren vanuit Django Models


Schemas zijn zeer nuttig voor het definiëren van validatieregels en responses, maar soms moet je je database modellen in schemas weerspiegelen en wijzigingen gesynchroniseerd houden.
## ModelSchema

`ModelSchema` is een speciale base class die automatisch een schema kan genereren vanuit je model.

Het enige wat je hoeft te doen is `model` en `fields` instellen op de `Meta` van je schema:


```python hl_lines="2 5 6 7"
from django.contrib.auth.models import User
from ninja import ModelSchema

class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

# Will create schema like this:
# 
# class UserSchema(Schema):
#     id: int
#     username: str
#     first_name: str
#     last_name: str
```

### Alle Modelfvelden Gebruiken

Om alle velden van een model te gebruiken — kun je `__all__` doorgeven aan `fields`:

```python hl_lines="4"
class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = "__all__"
```
!!! warning
    Het gebruik van __all__ wordt niet aanbevolen.
    <br>
    Dit kan leiden tot onbedoelde blootstelling van ongewenste data (zoals het gehashte wachtwoord in het voorbeeld hierboven).
    <br>
    Algemene aanbeveling - gebruik `fields` om expliciet de lijst met velden te definiëren die zichtbaar moeten zijn in je API.

### Modelfvelden Uitsluiten

Om alle velden te gebruiken **behalve** een beperkt aantal, kun je de `exclude` configuratie gebruiken:

```python hl_lines="4"
class UserSchema(ModelSchema):
    class Meta:
        model = User
        exclude = ['password', 'last_login', 'user_permissions']

# Will create schema like this:
# 
# class UserSchema(Schema):
#     id: int
#     username: str
#     first_name: str
#     last_name: str
#     email: str
#     is_superuser: bool
#     ... and the rest

```

### Velden Overriden

Om de standaardannotaties van bepaalde velden te wijzigen, of om nieuwe velden toe te voegen, gebruik je gewoon geannoteerde properties zoals gebruikelijk.
```python hl_lines="1 2 3 4 8"
class GroupSchema(ModelSchema):
    class Meta:
        model = Group
        fields = ['id', 'name']


class UserSchema(ModelSchema):
    groups: List[GroupSchema] = []

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

```


### Velden Optioneel Maken

Voor PATCH API operaties moet je doorgaans alle velden van een schema optioneel maken. Hiervoor kun je de configuratie fields_optional gebruiken

```python hl_lines="5"
class PatchGroupSchema(ModelSchema):
    class Meta:
        model = Group
        fields = ['id', 'name', 'description'] # Note: all these fields are required on model level
        fields_optional = '__all__'
```

Je kunt ook slechts een paar velden optioneel definiëren in plaats van alle velden:
```python
     fields_optional = ['description']
```

!!! done

    Ga verder naar het volgende hoofdstuk! **[Dynamisch een Schema Genereren](django-pydantic-create-schema.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
