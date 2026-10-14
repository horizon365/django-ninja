
Einige Verhaltensweisen von Ninja JWT können über Einstellungsvariablen in der `settings.py` angepasst werden:

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

Oben sind die Standardwerte dieser Einstellungen dargestellt.

## `ACCESS_TOKEN_LIFETIME`

Ein `datetime.timedelta`-Objekt, das die Lebensdauer der Access-Token angibt.
Bei der Token-Generierung wird dieser `timedelta`-Wert zur aktuellen UTC-Zeit addiert, um den Standardwert des `exp`-Claims des Tokens zu erhalten.

## `REFRESH_TOKEN_LIFETIME`

Ein `datetime.timedelta`-Objekt, das die Lebensdauer der Refresh-Token angibt.
Bei der Token-Generierung wird dieser `timedelta`-Wert zur aktuellen UTC-Zeit addiert, um den Standardwert des `exp`-Claims des Tokens zu erhalten.

### ``BLACKLIST_AFTER_ROTATION``
----------------------------
Wenn auf ``True`` gesetzt und die Blacklist-App verwendet wird sowie ``ROTATE_REFRESH_TOKENS`` auf ``True`` gesetzt ist,
werden Refresh-Token, die an ``TokenRefreshView`` übermittelt werden, auf die Blacklist gesetzt.
Um diese Einstellung zu verwenden, müssen Sie ``'ninja_jwt.token_blacklist'`` zu Ihren ``INSTALLED_APPS`` in Ihrer Settings-Datei hinzufügen.


Erfahren Sie mehr über `/blacklist_app`{.interpreted-text role="doc"}.

## `UPDATE_LAST_LOGIN`

Wenn auf `True` gesetzt, wird das Feld last_login in der Tabelle auth_user beim Login (TokenObtainPairView) aktualisiert.

    Warnung: Das Aktualisieren des letzten Logins erhöht die Anzahl der Datenbanktransaktionen erheblich.
    Missbrauch des Views kann den Server verlangsamen, was eine Sicherheitslücke darstellen kann.
    Wenn Sie dies wirklich tun möchten, drosseln Sie den Endpoint zumindest mit DRF.

## `ALGORITHM`

Der Algorithmus aus der PyJWT-Bibliothek, der für Signatur-/Verifizierungsoperationen an Token verwendet wird.
Für symmetrische HMAC-Signatur und -Verifizierung können Sie die folgenden Algorithmen verwenden: ``'HS256'``, ``'HS384'``,``'HS512'``.
Bei Auswahl eines HMAC-Algorithmus wird die Einstellung ``SIGNING_KEY`` sowohl als Signaturschlüssel als auch als Verifizierungsschlüssel verwendet.
In diesem Fall wird die Einstellung ``VERIFYING_KEY`` ignoriert.
Für asymmetrische RSA-Signatur und -Verifizierung können Sie die folgenden Algorithmen verwenden: ``'RS256'``, ``'RS384'``, ``'RS512'``.
Bei Auswahl eines RSA-Algorithmus muss die Einstellung ``SIGNING_KEY`` auf einen String gesetzt werden, der einen privaten RSA-Schlüssel enthält.
Ebenso muss die Einstellung ``VERIFYING_KEY`` auf einen String gesetzt werden, der einen öffentlichen RSA-Schlüssel enthält.

## `SIGNING_KEY`

Der Signaturschlüssel, der zum Signieren des Inhalts generierter Token verwendet wird.
Für die HMAC-Signatur sollte dies ein zufälliger String mit mindestens so vielen Datenbits sein, wie das Signaturverfahren erfordert.
Für die RSA-Signatur sollte dies ein String sein, der einen RSA-Privatschlüssel mit 2048 Bit oder mehr enthält.
Da Simple JWT standardmäßig die 256-Bit-HMAC-Signatur verwendet, enthält die Einstellung `SIGNING_KEY` standardmäßig den Wert der Einstellung `SECRET_KEY` Ihres Django-Projekts.
Obwohl dies die vernünftigste Voreinstellung ist, die Simple JWT bieten kann, wird Entwicklern empfohlen, diese Einstellung auf einen Wert zu ändern, der unabhängig vom geheimen Schlüssel des Django-Projekts ist.
Dadurch lässt sich der Signaturschlüssel leichter ändern, falls der für Token verwendete Signaturschlüssel kompromittiert wird.

## `VERIFYING_KEY`

Der Verifizierungsschlüssel, der zum Überprüfen des Inhalts generierter Token verwendet wird. Gibt die Einstellung ``ALGORITHM`` einen HMAC-Algorithmus an,
wird die Einstellung ``VERIFYING_KEY`` ignoriert und stattdessen der Wert von ``SIGNING_KEY`` verwendet.
Gibt die Einstellung ``ALGORITHM`` einen RSA-Algorithmus an, muss die Einstellung ``VERIFYING_KEY`` auf einen String gesetzt werden, der einen öffentlichen RSA-Schlüssel enthält.

## `AUDIENCE`

Der Audience-Claim, der in generierte Token aufgenommen und/oder in dekodierten Token verifiziert werden soll.
Bei ``None`` wird dieses Feld aus dem Token ausgeschlossen und nicht verifiziert.

## `ISSUER`

Der Issuer-Claim, der in generierte Token aufgenommen und/oder in dekodierten Token verifiziert werden soll.
Bei ``None`` wird dieses Feld aus dem Token ausgeschlossen und nicht verifiziert.

### ``JWK_URL``
----------

Die JWK_URL wird verwendet, um den zur Verifizierung der Tokensignaturen erforderlichen öffentlichen Schlüssel dynamisch aufzulösen.
Wenn Sie beispielsweise Auth0 verwenden, könnten Sie dies auf 'https://yourdomain.auth0.com/.well-known/jwks.json' setzen.
Bei ``None`` wird dieses Feld aus dem Token-Backend ausgeschlossen und während der Verifizierung nicht verwendet

### ``LEEWAY``
----------

Leeway (Toleranz) wird verwendet, um der Ablaufzeit etwas Spielraum zu geben. Dies kann eine ganzzahlige Anzahl von Sekunden oder ein ``datetime.timedelta`` sein.
Weitere Informationen finden Sie unter https://pyjwt.readthedocs.io/en/latest/usage.html#expiration-time-claim-exp

###``AUTH_HEADER_TYPES``
---------------------

Der/die für Views, die eine Authentifizierung erfordern, akzeptierten Autorisierungs-Header-Typ(en). Ein Wert von ``'Bearer'`` bedeutet beispielsweise, dass Views, die eine Authentifizierung erfordern, nach einem Header im folgenden Format suchen:
``Authorization: Bearer <token>``. Diese Einstellung kann auch eine Liste oder ein Tupel möglicher Header-Typen enthalten (z. B. ``('Bearer', 'JWT')``).
Wird eine Liste oder ein Tupel auf diese Weise verwendet und schlägt die Authentifizierung fehl, wird das erste Element der Sammlung verwendet, um den „WWW-Authenticate"-Header in der Antwort zu konstruieren.

###``AUTH_HEADER_NAME``
----------------------------

Der Name des für die Authentifizierung verwendeten Autorisierungs-Headers. Der Standardwert ist `HTTP_AUTHORIZATION`, wodurch der `Authorization`-Header aus Requests akzeptiert wird.
Wenn Sie beispielsweise `X_Access_Token` in Ihren Request-Headern verwenden möchten, geben Sie `AUTH_HEADER_NAME` als `HTTP_X_ACCESS_TOKEN` in Ihren Einstellungen an.


###``USER_ID_FIELD``
-----------------

Das Datenbankfeld im Benutzermodell, das in generierte Token aufgenommen wird, um den Benutzer zu identifizieren.
Es wird empfohlen, dass der Wert dieser Einstellung ein Feld angibt, das sich nach Festlegung seines Anfangswerts typischerweise nicht mehr ändert.
Die Angabe eines Feldes „username" oder „email" wäre beispielsweise eine schlechte Wahl,
da sich der Benutzername oder die E-Mail eines Kontos je nach Gestaltung der Kontoverwaltung im jeweiligen Dienst ändern kann.
Dies könnte es ermöglichen, ein neues Konto mit einem alten Benutzernamen zu erstellen, während bestehende Token, die diesen Benutzernamen als Benutzerkennung verwenden, gültig bleiben.

###``USER_ID_CLAIM``
-----------------

Der Claim, der zum Speichern der Benutzerkennung in generierten Token verwendet wird. Wird der Wert beispielsweise auf ```"user_id"``` gesetzt, enthält das generierte Token einen „user_id"-Claim,
der die Kennung des Benutzers enthält.

###``USER_AUTHENTICATION_RULE``
----------------------------

Ein Callable, das bestimmt, ob der Benutzer zur Authentifizierung zugelassen ist. Diese Regel wird angewendet, nachdem ein gültiges Token verarbeitet wurde. Das Benutzerobjekt wird als Argument an das Callable übergeben.
Die Standardregel prüft, ob das Flag ``is_active`` noch ``True`` ist.
Das Callable muss einen booleschen Wert zurückgeben; ``True`` bedeutet autorisiert, andernfalls ``False``, was zu einem Statuscode 401 führt.

###``AUTH_TOKEN_CLASSES``
----------------------

Eine Liste von gepunkteten Pfaden, die auf Klassen verweisen, welche die zugelassenen Token-Typen zum Nachweis der Authentifizierung angeben. Weitere Informationen im Abschnitt „Token-Typen" unten.

###``TOKEN_TYPE_CLAIM``
--------------------

Der Name des Claims, der zum Speichern des Token-Typs verwendet wird. Weitere Informationen im Abschnitt „Token-Typen" unten.

###``JTI_CLAIM``
-------------

Der Name des Claims, der zum Speichern des eindeutigen Bezeichners des Tokens verwendet wird. Dieser Bezeichner wird verwendet, um widerrufene Token in der Blacklist-App zu identifizieren.
In einigen Fällen kann es erforderlich sein, einen anderen Claim als den Standard-Claim „jti" zu verwenden, um einen solchen Wert zu speichern.

###``TOKEN_USER_CLASS``
--------------------

Ein zustandsloses Benutzerobjekt, das von einem verifizierten Token unterstützt wird. Wird nur vom Authentifizierungs-Backend JWTStatelessUser verwendet.
Der Wert ist ein gepunkteter Pfad, der auf Ihre Unterklasse von ``"rest_framework_simplejwt.models.TokenUser"`` verweist, die auch der Standardwert ist.

###``SLIDING_TOKEN_LIFETIME``
--------------------------

Ein ``datetime.timedelta``-Objekt, das angibt, wie lange ein Sliding-Token zum Nachweis der Authentifizierung gültig ist.
Bei der Token-Generierung wird dieser ``timedelta``-Wert zur aktuellen UTC-Zeit addiert, um den Standardwert des „exp"-Claims des Tokens zu erhalten.
Weitere Informationen im Abschnitt „Sliding Tokens" unten.

###``SLIDING_TOKEN_REFRESH_LIFETIME``
----------------------------------

Ein ``datetime.timedelta``-Objekt, das angibt, wie lange ein Sliding-Token zur Erneuerung gültig ist.
Bei der Token-Generierung wird dieser `timedelta`-Wert zur aktuellen UTC-Zeit addiert, um den Standardwert des „exp"-Claims des Tokens zu erhalten.
Weitere Informationen im Abschnitt „Sliding Tokens" unten.

###``SLIDING_TOKEN_REFRESH_EXP_CLAIM``
-----------------------------------

Der Name des Claims, der zum Speichern der Ablaufzeit des Erneuerungszeitraums eines Sliding-Tokens verwendet wird. Weitere Informationen im Abschnitt „Sliding Tokens" unten.

!!! success

    Fahren Sie mit dem nächsten Kapitel fort: **[Token-Claims anpassen](customizing_token_claims.md)**.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
