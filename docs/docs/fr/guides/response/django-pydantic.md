---
comments: true
---
# Génération de Schemas à partir des models Django


Les Schemas sont très utiles pour définir des règles de validation et des réponses, mais parfois vous devez refléter vos models de base de données dans des schémas et maintenir les modifications synchronisées.
## ModelSchema

`ModelSchema` est une classe de base spéciale qui peut générer automatiquement un schéma à partir de votre model.

Tout ce que vous avez à faire est de définir `model` et `fields` dans le `Meta` de votre schéma :


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

### Utilisation de tous les champs du model

Pour utiliser tous les champs d'un model — vous pouvez passer `__all__` à `fields` :

```python hl_lines="4"
class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = "__all__"
```
!!! warning
    L'utilisation de __all__ n'est pas recommandée.
    <br>
    Cela peut conduire à une exposition accidentelle de données non souhaitées (telles que le mot de passe haché dans l'exemple ci-dessus).
    <br>
    Recommandation générale - utilisez `fields` pour définir explicitement la liste des champs que vous souhaitez rendre visibles dans votre API.

### Exclusion de champs du model

Pour utiliser tous les champs **sauf** quelques-uns, vous pouvez utiliser la configuration `exclude` :

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

### Redéfinition des champs

Pour modifier les annotations par défaut de certains champs, ou pour ajouter de nouveaux champs, utilisez simplement les propriétés annotées comme d'habitude.
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


### Rendre des champs optionnels

Pour les opérations d'API PATCH, vous avez généralement besoin de rendre tous les champs d'un schéma optionnels. Pour ce faire, vous pouvez utiliser la configuration fields_optional

```python hl_lines="5"
class PatchGroupSchema(ModelSchema):
    class Meta:
        model = Group
        fields = ['id', 'name', 'description'] # Note: all these fields are required on model level
        fields_optional = '__all__'
```

Vous pouvez également définir seulement quelques champs optionnels au lieu de tous :
```python
     fields_optional = ['description']
```

!!! done

    Poursuivez avec le chapitre suivant ! **[Génération dynamique d'un Schema](django-pydantic-create-schema.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
