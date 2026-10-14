
Ninja JWT wird mit einer Anwendung ausgeliefert, die eine Token-Blacklist-Funktionalität bereitstellt.
Um diese Anwendung zu verwenden, nehmen Sie sie in die Liste der installierten Anwendungen in der `settings.py` auf:

```python
# Django project settings.py

...

INSTALLED_APPS = (
    ...
    'ninja_jwt.token_blacklist',
    ...
)
```

Stellen Sie außerdem sicher, dass Sie `python manage.py migrate` ausführen, um die Migrationen der Anwendung auszuführen.

Wenn die Blacklist-Anwendung in `INSTALLED_APPS` erkannt wird, fügt Ninja JWT alle generierten Refresh-Token oder Sliding-Token zur Liste der ausstehenden Token (outstanding tokens) hinzu.
Außerdem prüft es, bevor ein Refresh-Token oder Sliding-Token als gültig angesehen wird, ob das Token nicht in der Token-Blacklist erscheint.

Die Ninja-JWT-Blacklist-Anwendung verwendet zwei Modelle: `OutstandingToken` und `BlacklistedToken`, um ihre Listen ausstehender Token und Blacklist-Token zu implementieren.
Für beide Modelle sind Model-Admins definiert. Um ein Token auf die Blacklist zu setzen, suchen Sie den entsprechenden `OutstandingToken`-Datensatz im Admin,
und erstellen Sie dann erneut über den Admin einen `BlacklistedToken`-Datensatz, der auf den `OutstandingToken`-Datensatz verweist.

Alternativ können Sie ein Token auf die Blacklist setzen, indem Sie eine Instanz einer `BlacklistMixin`-Unterklasse erstellen und die Methode `blacklist` auf dieser Instanz aufrufen:

```python
from ninja_jwt.tokens import RefreshToken

token = RefreshToken(base64_encoded_token_string)
token.blacklist()
```

Dies erstellt einen eindeutigen Outstanding-Token- und Blacklist-Datensatz für den `jti`-Claim des Tokens oder für den Claim, der in der Einstellung `JTI_CLAIM` angegeben ist.

Die Blacklist-Anwendung stellt außerdem einen Management-Befehl `flushexpiredtokens` bereit, der abgelaufene Token sowohl aus der Outstanding-Liste als auch aus der Blacklist entfernt.
Sie sollten auf Ihrem Server oder Ihrer Hosting-Plattform einen Cron-Job einrichten, der diesen Befehl täglich ausführt.

!!! success

    Fahren Sie mit dem nächsten Kapitel fort: **[Entwicklung und Mitarbeit](development_and_contributing.md)**.


<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
