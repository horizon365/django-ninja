
Certains comportements de Ninja JWT peuvent être personnalisés via des variables de paramètres dans `settings.py` :

```python
# Django project settings.py

from datetime import timedelta
from django.conf import settings
...

NINJA_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': settings.SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'ninja_jwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('ninja_jwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'ninja_jwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    
    # For Controller Schemas
    # FOR OBTAIN PAIR
    'TOKEN_OBTAIN_PAIR_INPUT_SCHEMA': "ninja_jwt.schema.TokenObtainPairInputSchema",
    'TOKEN_OBTAIN_PAIR_REFRESH_INPUT_SCHEMA': "ninja_jwt.schema.TokenRefreshInputSchema",
    # FOR SLIDING TOKEN
    'TOKEN_OBTAIN_SLIDING_INPUT_SCHEMA': "ninja_jwt.schema.TokenObtainSlidingInputSchema",
    'TOKEN_OBTAIN_SLIDING_REFRESH_INPUT_SCHEMA':"ninja_jwt.schema.TokenRefreshSlidingInputSchema",
    
    'TOKEN_BLACKLIST_INPUT_SCHEMA': "ninja_jwt.schema.TokenBlacklistInputSchema",
    'TOKEN_VERIFY_INPUT_SCHEMA': "ninja_jwt.schema.TokenVerifyInputSchema",
}
```

Ci-dessus, les valeurs par défaut de ces paramètres sont affichées.

## `ACCESS_TOKEN_LIFETIME`

Un objet `datetime.timedelta` qui spécifie la durée de vie des access tokens.
Lors de la génération du token, cette valeur `timedelta` est ajoutée à l'heure UTC actuelle pour obtenir la valeur par défaut de la claim `exp` du token.

## `REFRESH_TOKEN_LIFETIME`

Un objet `datetime.timedelta` qui spécifie la durée de vie des refresh tokens.
Lors de la génération du token, cette valeur `timedelta` est ajoutée à l'heure UTC actuelle pour obtenir la valeur par défaut de la claim `exp` du token.

### ``BLACKLIST_AFTER_ROTATION``
----------------------------
Lorsqu'il est défini sur ``True``, si l'application de blacklist est utilisée et que ``ROTATE_REFRESH_TOKENS`` est défini sur ``True``,
les refresh tokens soumis à ``TokenRefreshView`` seront ajoutés à la blacklist.
Vous devez ajouter ``'ninja_jwt.token_blacklist'`` à votre ``INSTALLED_APPS`` dans votre fichier de settings pour utiliser ce paramètre.


En savoir plus sur `/blacklist_app`{.interpreted-text role="doc"}.

## `UPDATE_LAST_LOGIN`

Lorsqu'il est défini sur `True`, le champ last_login de la table auth_user est mis à jour lors de la connexion (TokenObtainPairView).

    Avertissement : la mise à jour du last login augmentera considérablement le nombre de transactions en base de données.
    Les utilisateurs abusant de la vue peuvent ralentir le serveur, ce qui peut constituer une vulnérabilité de sécurité.
    Si vous voulez vraiment faire cela, limitez au moins le débit de l'endpoint avec DRF.

## `ALGORITHM`

L'algorithme utilisé de la bibliothèque PyJWT pour effectuer les opérations de signature/vérification sur les tokens.
Pour utiliser la signature et la vérification symétriques HMAC, vous pouvez utiliser les algorithmes suivants : ``'HS256'``, ``'HS384'``,``'HS512'``.
Lors de la sélection d'un algorithme HMAC, le paramètre ``SIGNING_KEY`` sera utilisé à la fois comme clé de signature et comme clé de vérification.
Dans ce cas, le paramètre ``VERIFYING_KEY`` est ignoré.
Pour utiliser la signature et la vérification asymétriques RSA, vous pouvez utiliser les algorithmes suivants : ``'RS256'``, ``'RS384'``, ``'RS512'``.
Lors de la sélection d'un algorithme RSA, le paramètre ``SIGNING_KEY`` doit être défini sur une chaîne contenant une clé privée RSA.
De même, le paramètre ``VERIFYING_KEY`` doit être défini sur une chaîne contenant une clé publique RSA.

## `SIGNING_KEY`

La clé de signature utilisée pour signer le contenu des tokens générés.
Pour la signature HMAC, il doit s'agir d'une chaîne aléatoire contenant au moins autant de bits de données que ce qu'exige le protocole de signature.
Pour la signature RSA, il doit s'agir d'une chaîne contenant une clé privée RSA de 2048 bits ou plus.
Comme Simple JWT utilise par défaut une signature HMAC de 256 bits, le paramètre `SIGNING_KEY` prend par défaut la valeur du paramètre `SECRET_KEY` de votre projet Django.
Bien qu'il s'agisse de la valeur par défaut la plus raisonnable que Simple JWT puisse fournir, il est recommandé aux développeurs de modifier ce paramètre pour une valeur indépendante de la clé secrète du projet Django.
Cela facilitera le changement de la clé de signature dans l'éventualité où la clé de signature utilisée pour les tokens serait compromise.

## `VERIFYING_KEY`

La clé de vérification utilisée pour vérifier le contenu des tokens générés. Si le paramètre ``ALGORITHM`` spécifie un algorithme HMAC,
le paramètre ``VERIFYING_KEY`` est ignoré et la valeur de ``SIGNING_KEY`` est utilisée à la place.
Si le paramètre ``ALGORITHM`` spécifie un algorithme RSA, le paramètre ``VERIFYING_KEY`` doit être défini sur une chaîne contenant une clé publique RSA.

## `AUDIENCE`

La claim audience à inclure dans les tokens générés et/ou à vérifier dans les tokens décodés.
Lorsqu'il est défini sur ``None``, ce champ est exclu du token et non vérifié.

## `ISSUER`

La claim issuer à inclure dans les tokens générés et/ou à vérifier dans les tokens décodés.
Lorsqu'il est défini sur ``None``, ce champ est exclu du token et non vérifié.

### ``JWK_URL``
----------

Le JWK_URL est utilisé pour résoudre dynamiquement la clé publique nécessaire à la vérification des signatures de tokens.
Par exemple, lors de l'utilisation d'Auth0, vous pourriez définir ceci sur 'https://yourdomain.auth0.com/.well-known/jwks.json'.
Lorsqu'il est défini sur ``None``, ce champ est exclu du backend de tokens et non utilisé lors de la vérification

### ``LEEWAY``
----------

La marge (leeway) est utilisée pour donner une certaine tolérance au délai d'expiration. Il peut s'agir d'un nombre entier de secondes ou d'un ``datetime.timedelta``.
Veuillez consulter https://pyjwt.readthedocs.io/en/latest/usage.html#expiration-time-claim-exp pour plus d'informations.

###``AUTH_HEADER_TYPES``
---------------------

Le ou les types d'en-tête d'autorisation qui seront acceptés pour les vues nécessitant une authentification. Par exemple, une valeur de ``'Bearer'`` signifie que les vues nécessitant une authentification rechercheront un en-tête au format suivant :
``Authorization: Bearer <token>``. Ce paramètre peut également contenir une liste ou un tuple de types d'en-tête possibles (par exemple ``('Bearer', 'JWT')``).
Si une liste ou un tuple est utilisé de cette manière et que l'authentification échoue, le premier élément de la collection sera utilisé pour construire l'en-tête « WWW-Authenticate » dans la réponse.

###``AUTH_HEADER_NAME``
----------------------------

Le nom de l'en-tête d'autorisation utilisé pour l'authentification. La valeur par défaut est `HTTP_AUTHORIZATION`, qui acceptera l'en-tête `Authorization` des requêtes.
Par exemple, si vous souhaitez utiliser `X_Access_Token` dans vos en-têtes de requête, spécifiez `AUTH_HEADER_NAME` comme `HTTP_X_ACCESS_TOKEN` dans vos settings.


###``USER_ID_FIELD``
-----------------

Le champ de la base de données dans le modèle utilisateur qui sera inclus dans les tokens générés pour identifier l'utilisateur.
Il est recommandé que la valeur de ce paramètre spécifie un champ qui ne change généralement pas une fois sa valeur initiale choisie.
Par exemple, spécifier un champ « username » ou « email » serait un mauvais choix,
car le username ou l'email d'un compte peut changer selon la manière dont la gestion des comptes est conçue dans un service donné.
Cela pourrait permettre à un nouveau compte d'être créé avec un ancien username, tandis que les tokens existants qui utilisent ce username comme identifiant utilisateur restent valides.

###``USER_ID_CLAIM``
-----------------

La claim utilisée pour stocker l'identifiant de l'utilisateur dans les tokens générés. Par exemple, définir la valeur sur ```"user_id"``` signifie que le token généré contient une claim « user_id »,
qui contient l'identifiant de l'utilisateur.

###``USER_AUTHENTICATION_RULE``
----------------------------

Un appelable utilisé pour déterminer si l'utilisateur est autorisé à s'authentifier. Cette règle est appliquée après le traitement d'un token valide. L'objet utilisateur est passé en argument à l'appelable.
La règle par défaut consiste à vérifier que le flag ``is_active`` est toujours ``True``.
L'appelable doit renvoyer une valeur booléenne, ``True`` signifiant autorisé, ``False`` entraînant sinon un code de statut 401.

###``AUTH_TOKEN_CLASSES``
----------------------

Une liste de chemins pointés désignant les classes qui spécifient les types de tokens autorisés pour prouver l'authentification. Plus d'informations dans la section « Types de tokens » ci-dessous.

###``TOKEN_TYPE_CLAIM``
--------------------

Le nom de la claim utilisée pour stocker le type de token. Plus d'informations dans la section « Types de tokens » ci-dessous.

###``JTI_CLAIM``
-------------

Le nom de la claim utilisée pour stocker l'identifiant unique du token. Cet identifiant est utilisé pour identifier les tokens révoqués dans l'application de blacklist.
Dans certains cas, il peut être nécessaire d'utiliser une claim autre que la claim « jti » par défaut pour stocker cette valeur.

###``TOKEN_USER_CLASS``
--------------------

Un objet utilisateur sans état adossé à un token vérifié. Utilisé uniquement par le backend d'authentification JWTStatelessUser.
La valeur est un chemin pointé désignant votre sous-classe de ``"rest_framework_simplejwt.models.TokenUser"``, qui constitue également la valeur par défaut.

###``SLIDING_TOKEN_LIFETIME``
--------------------------

Un objet ``datetime.timedelta`` qui spécifie la durée de validité d'un sliding token pour prouver l'authentification.
Lors de la génération du token, cette valeur ``timedelta`` est ajoutée à l'heure UTC actuelle pour obtenir la valeur par défaut de la claim « exp » du token.
Plus d'informations dans la section « Sliding Tokens » ci-dessous.

###``SLIDING_TOKEN_REFRESH_LIFETIME``
----------------------------------

Un objet ``datetime.timedelta`` qui spécifie la durée de validité d'un sliding token pour être rafraîchi.
Lors de la génération du token, cette valeur `timedelta` est ajoutée à l'heure UTC actuelle pour obtenir la valeur par défaut de la claim « exp » du token.
Plus d'informations dans la section « Sliding Tokens » ci-dessous.

###``SLIDING_TOKEN_REFRESH_EXP_CLAIM``
-----------------------------------

Le nom de la claim utilisée pour stocker le délai d'expiration de la période de rafraîchissement d'un sliding token. Plus d'informations dans la section « Sliding Tokens » ci-dessous.

!!! success

    Poursuivez avec le chapitre suivant **[Personnalisation des claims de tokens](customizing_token_claims.md)**.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
