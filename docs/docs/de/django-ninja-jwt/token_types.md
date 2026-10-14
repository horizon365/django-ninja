
Ninja JWT bietet zwei verschiedene Tokentypen, die zum Nachweis der Authentifizierung verwendet werden können.
Im Payload eines Tokens lässt sich sein Typ am Wert des Token-Typ-Claims erkennen, der standardmäßig `token_type` heißt.
Dort kann jedoch einer der Werte `access`, `sliding` oder `refresh` stehen,
wobei Refresh-Tokens derzeit nicht als gültige Authentifizierungs-Tokens gelten. Der Name des Claims, in dem der Typ gespeichert wird, lässt sich über die Einstellung `TOKEN_TYPE_CLAIM` anpassen.

Standardmäßig erwartet Ninja JWT ein `access`-Token zum Nachweis der Authentifizierung.
Die zulässigen Authentifizierungs-Tokentypen werden über den Wert der Einstellung `AUTH_TOKEN_CLASSES` bestimmt.
Diese Einstellung enthält eine Liste von Dotted Paths, die auf Token-Klassen verweisen. Standardmäßig enthält sie den Dotted Path `'ninja_jwt.tokens.AccessToken'`,
kann aber auch den Dotted Path `'ninja_jwt.tokens.SlidingToken'` umfassen.
Einer oder beide dieser Dotted Paths können in der Liste der Authentifizierungs-Token-Klassen enthalten sein.
Wenn beide vorhanden sind, können beide Tokentypen zum Nachweis der Authentifizierung verwendet werden.

Sliding Tokens
==============

Sliding Tokens bieten Token-Nutzern einen bequemeren Umgang, erfordern aber Abstriche bei der Sicherheit und – wenn die Blacklist-App verwendet wird – bei der Performance.
Ein Sliding-Token ist ein Token, das sowohl einen Expiration-Claim als auch einen Refresh-Expiration-Claim enthält. Solange der Zeitstempel im Expiration-Claim des Sliding-Tokens noch nicht abgelaufen ist,
kann es zum Nachweis der Authentifizierung verwendet werden. Darüber hinaus kann es, solange der Zeitstempel in seinem Refresh-Expiration-Claim noch nicht abgelaufen ist,
auch an die Refresh-View übermittelt werden, um eine Kopie seiner selbst mit aktualisiertem Expiration-Claim zu erhalten.

Wenn Sie Sliding Tokens verwenden möchten, ändern Sie die Einstellung `AUTH_TOKEN_CLASSES` zu `('ninja_jwt.tokens.SlidingToken',)`.
(Alternativ können Sie – wenn Sie beide Tokentypen für die Authentifizierung zulassen möchten – in der Einstellung `AUTH_TOKEN_CLASSES` Dotted Paths auf die Token-Klassen `AccessToken` und `SlidingToken`
im Modul `ninja_jwt.tokens` aufnehmen)

Registrieren Sie außerdem `NinjaJWTSlidingController` bei der `api`:
```python
from ninja_jwt.controller import NinjaJWTSlidingController
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTSlidingController)

```

Beachten Sie, dass Ninja JWT bei Verwendung der Blacklist-App alle Sliding Tokens bei jedem authentifizierten Request gegen die Blacklist prüft.
Dies verschlechtert die Performance der authentifizierten API-Views.

!!! success

    Fahren Sie mit dem nächsten Kapitel fort: **[Blacklist App](blacklist_app.md)**.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
