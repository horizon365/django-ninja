---
comments: true
---
# Schemata aus Django-Modellen generieren


Schemata sind sehr nützlich, um Validierungsregeln und Responses zu definieren, aber manchmal müssen Sie Ihre Datenbankmodelle in Schemata abbilden und Änderungen synchron halten.
## ModelSchema

`ModelSchema` ist eine spezielle Basisklasse, die automatisch ein Schema aus Ihrem Modell generieren kann.

Alles, was Sie tun müssen, ist `model` und `fields` in der `Meta` Ihres Schemas zu setzen:


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

### Alle Modellfelder verwenden

Um alle Felder eines Modells zu verwenden – können Sie `__all__` an `fields` übergeben:

```python hl_lines="4"
class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = "__all__"
```
!!! warning
    Die Verwendung von __all__ wird nicht empfohlen.
    <br>
    Das kann dazu führen, dass versehentlich unerwünschte Daten offengelegt werden (wie etwa das gehashte Passwort im obigen Beispiel).
    <br>
    Allgemeine Empfehlung – verwenden Sie `fields`, um die Liste der Felder explizit zu definieren, die in Ihrer API sichtbar sein sollen.

### Modellfelder ausschließen

Um alle Felder **außer** einigen wenigen zu verwenden, können Sie die Konfiguration `exclude` nutzen:

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

### Felder überschreiben

Um die Standardannotationen für einige Felder zu ändern oder neue Felder hinzuzufügen, verwenden Sie einfach wie üblich annotierte Properties.
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


### Felder optional machen

Bei PATCH-API-Operationen müssen Sie typischerweise alle Felder eines Schemas optional machen. Dazu können Sie die Konfiguration `fields_optional` verwenden

```python hl_lines="5"
class PatchGroupSchema(ModelSchema):
    class Meta:
        model = Group
        fields = ['id', 'name', 'description'] # Note: all these fields are required on model level
        fields_optional = '__all__'
```

Sie können auch nur einzelne Felder optional definieren, statt aller:
```python
     fields_optional = ['description']
```

!!! done

    Weiter zum nächsten Kapitel! **[Ein Schema dynamisch generieren](django-pydantic-create-schema.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
