---
comments: true
---
Si vous ne savez pas comment gérer les requêtes POST avec des types de contenu comme `application/x-www-form-urlencoded` ou `multipart/form-data` dans django-ninja-extra, alors ce guide vous sera utile.
Django-Ninja couvre déjà la plupart des cas d'utilisation [ici](https://django-ninja.cn/tutorial/form-params/), mais je vais vous en faire un bref résumé ici.

### Données de formulaire en tant que paramètres

```python hl_lines="7 8"
from ninja import Form, constants
from ninja_extra import api_controller, http_post


@api_controller('', tags=['My Operations'], auth=constants.NOT_SET, permissions=[])
class MyAPIController:
    @http_post("/login")
    def login(self, username: str = Form(...), password: str = Form(...)):
        return {'username': username, 'password': '*****'}
```
Deux points sont à noter ici :

- Vous devez importer `Form` depuis le module `ninja`
- Utilisez `Form` comme valeur par défaut pour vos paramètres


!!! info
    Pour plus d'informations à ce sujet, consultez le [Tutoriel sur les formulaires de Django-Ninja](https://django-ninja.cn/guides/input/form-params/)
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
