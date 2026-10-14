---
comments: true
---
# Téléversement de fichiers

La gestion des fichiers ne diffère pas de la gestion des autres paramètres.

```python hl_lines="1 2 5"
from ninja import NinjaAPI, File
from ninja.files import UploadedFile

@api.post("/upload")
def upload(request, file: UploadedFile = File(...)):
    data = file.read()
    return {'name': file.name, 'len': len(data)}
```


`UploadedFile` est un alias pour [l'UploadFile de Django](https://docs.djangoproject.com/en/stable/ref/files/uploads/#django.core.files.uploadedfile.UploadedFile), qui possède toutes les méthodes et attributs pour accéder au fichier téléversé.

 - read()
 - multiple_chunks(chunk_size=None)
 - chunks(chunk_size=None)
 - name
 - size
 - content_type
 - content_type_extra
 - charset
 - etc.

## Téléversement de plusieurs fichiers

Pour **téléverser plusieurs fichiers** à la fois, déclarez simplement une `List` de `UploadedFile` :


```python hl_lines="1 6"
from typing import List
from ninja import NinjaAPI, File
from ninja.files import UploadedFile

@api.post("/upload-many")
def upload_many(request, files: List[UploadedFile] = File(...)):
    return [f.name for f in files]
```

## Téléversement de fichiers avec des champs supplémentaires
Remarque : le protocole HTTP ne permet pas d'envoyer des fichiers au format `application/json` par défaut (sauf si vous effectuez un encodage JSON côté client).

Pour envoyer un fichier avec des propriétés supplémentaires, vous devez envoyer le corps avec l'encodage `multipart/form-data`. Vous pouvez le faire simplement en marquant les champs comme `Form` :

```python hl_lines="14"
from ninja import NinjaAPI, Schema, UploadedFile, Form, File
from datetime import date

api = NinjaAPI()


class UserDetails(Schema):
    first_name: str
    last_name: str
    birthdate: date


@api.post('/users')
def create_user(request, details: Form[UserDetails], file: File[UploadedFile]):
    return [details.dict(), file.name]

```

Remarque : dans ce cas, tous les champs doivent être envoyés comme champs de formulaire.

Vous pouvez également envoyer la charge utile (payload) sous la forme d'un seul champ JSON — supprimez simplement le marqueur `Form` :


```python
@api.post('/users')
def create_user(request, details: UserDetails, file: File[UploadedFile]):
    return [details.dict(), file.name]

```

Cela attendra que le client envoie les données sous la forme `multipart/form-data` avec 2 champs :

  - details : le JSON sous forme de chaîne
  - file : le fichier


### Une liste de fichiers avec des informations supplémentaires

```python
@api.post('/users')
def create_user(request, details: Form[UserDetails], files: File[list[UploadedFile]]):
    return [details.dict(), [f.name for f in files]]
```
!!! done

    Poursuivez avec le chapitre suivant ! **[Analyseurs de requête](request-parsers.md)**

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
