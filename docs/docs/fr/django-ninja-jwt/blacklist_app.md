
Ninja JWT est livré avec une application qui fournit une fonctionnalité de blacklist de tokens.
Pour utiliser cette application, incluez-la dans la liste des applications installées dans `settings.py` :

```python
# Django project settings.py

...

INSTALLED_APPS = (
    ...
    'ninja_jwt.token_blacklist',
    ...
)
```

Assurez-vous également d'exécuter `python manage.py migrate` pour appliquer les migrations de l'application.

Si l'application de blacklist est détectée dans `INSTALLED_APPS`, Ninja JWT ajoutera tous les refresh tokens ou sliding tokens générés à la liste des tokens outstanding.
Il vérifiera également, avant de considérer tout refresh token ou sliding token comme valide, que le token n'apparaît pas dans la blacklist de tokens.

L'application de blacklist de Ninja JWT utilise deux modèles : `OutstandingToken` et `BlacklistedToken` pour implémenter ses listes de tokens outstanding et de blacklist.
Des model admins sont définis pour les deux modèles. Pour ajouter un token à la blacklist, trouvez son enregistrement `OutstandingToken` correspondant dans l'admin,
puis utilisez à nouveau l'admin pour créer un enregistrement `BlacklistedToken` qui pointe vers l'enregistrement `OutstandingToken`.

Alternativement, vous pouvez blacklister un token en créant une instance d'une sous-classe de `BlacklistMixin` et en appelant la méthode `blacklist` sur cette instance :

```python
from ninja_jwt.tokens import RefreshToken

token = RefreshToken(base64_encoded_token_string)
token.blacklist()
```

Cela créera un token outstanding unique et un enregistrement de blacklist pour la claim `jti` du token, ou pour la claim spécifiée par le paramètre `JTI_CLAIM`.

L'application de blacklist fournit également une commande de gestion `flushexpiredtokens`, qui supprimera tous les tokens expirés de la liste outstanding et de la blacklist.
Vous devriez configurer un cron job sur votre serveur ou votre plateforme d'hébergement qui exécute cette commande quotidiennement.

!!! success

    Poursuivez avec le chapitre suivant **[Développement et contribution](development_and_contributing.md)**.


<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
