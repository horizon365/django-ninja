
Sommige aspecten van het gedrag van Ninja JWT kunnen worden aangepast via instellingsvariabelen in `settings.py`:

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

Hierboven worden de standaardwaarden voor deze instellingen getoond.

## `ACCESS_TOKEN_LIFETIME`

Een object `datetime.timedelta` dat de levensduur van access tokens specificeert.
Tijdens het genereren van tokens wordt deze `timedelta`-waarde opgeteld bij de huidige UTC-tijd om de standaard `exp`-claimwaarde van het token te verkrijgen.

## `REFRESH_TOKEN_LIFETIME`

Een object `datetime.timedelta` dat de levensduur van refresh tokens specificeert.
Tijdens het genereren van tokens wordt deze `timedelta`-waarde opgeteld bij de huidige UTC-tijd om de standaard `exp`-claimwaarde van het token te verkrijgen.

### ``BLACKLIST_AFTER_ROTATION``
----------------------------
Wanneer ingesteld op ``True``, en de blacklist-app is in gebruik en ``ROTATE_REFRESH_TOKENS`` is ingesteld op ``True``,
worden refresh tokens die worden ingediend bij ``TokenRefreshView`` toegevoegd aan de blacklist.
Je moet ``'ninja_jwt.token_blacklist'`` toevoegen aan je ``INSTALLED_APPS`` in je instellingenbestand om deze instelling te gebruiken.


Lees meer over `/blacklist_app`{.interpreted-text role="doc"}.

## `UPDATE_LAST_LOGIN`

Wanneer ingesteld op `True`, wordt het veld last_login in de tabel auth_user bijgewerkt bij het inloggen (TokenObtainPairView).

    Waarschuwing: Het bijwerken van de laatste login verhoogt het aantal databasetransacties aanzienlijk.
    Misbruikers van de view kunnen de server vertragen, wat een beveiligingskwetsbaarheid kan zijn.
    Als je dit echt wilt doen, throttle het endpoint dan ten minste met DRF.

## `ALGORITHM`

Het algoritme uit de PyJWT-library dat wordt gebruikt om ondertekenings-/verificatieoperaties op tokens uit te voeren.
Voor symmetrische HMAC-ondertekening en -verificatie kun je de volgende algoritmen gebruiken: ``'HS256'``, ``'HS384'``,``'HS512'``.
Bij het kiezen van een HMAC-algoritme wordt de instelling ``SIGNING_KEY`` gebruikt als zowel de ondertekeningssleutel als de verificatiesleutel.
In dat geval wordt de instelling ``VERIFYING_KEY`` genegeerd.
Voor asymmetrische RSA-ondertekening en -verificatie kun je de volgende algoritmen gebruiken: ``'RS256'``, ``'RS384'``, ``'RS512'``.
Bij het kiezen van een RSA-algoritme moet de instelling ``SIGNING_KEY`` worden ingesteld op een string die een RSA-privésleutel bevat.
Evenzo moet de instelling ``VERIFYING_KEY`` worden ingesteld op een string die een RSA-openbare sleutel bevat.

## `SIGNING_KEY`

De ondertekeningssleutel die wordt gebruikt om de inhoud van gegenereerde tokens te ondertekenen.
Voor HMAC-ondertekening moet dit een willekeurige string zijn met ten minste zoveel bits aan gegevens als het ondertekeningsprotocol vereist.
Voor RSA-ondertekening moet dit een string zijn met een RSA-privésleutel van 2048 bits of langer.
Aangezien Simple JWT standaard 256-bit HMAC-ondertekening gebruikt, is de instelling `SIGNING_KEY` standaard de waarde van de instelling `SECRET_KEY` van je Django-project.
Hoewel dit de meest redelijke standaardwaarde is die Simple JWT kan bieden, wordt ontwikkelaars aangeraden deze instelling te wijzigen in een waarde die onafhankelijk is van de geheime sleutel van het Django-project.
Dit maakt het eenvoudiger om de ondertekeningssleutel te wijzigen in het geval dat de voor tokens gebruikte ondertekeningssleutel gecompromitteerd raakt.

## `VERIFYING_KEY`

De verificatiesleutel die wordt gebruikt om de inhoud van gegenereerde tokens te verifiëren. Als de instelling ``ALGORITHM`` een HMAC-algoritme specificeert,
wordt de instelling ``VERIFYING_KEY`` genegeerd en wordt in plaats daarvan de waarde van ``SIGNING_KEY`` gebruikt.
Als de instelling ``ALGORITHM`` een RSA-algoritme specificeert, moet de instelling ``VERIFYING_KEY`` worden ingesteld op een string die een RSA-openbare sleutel bevat.

## `AUDIENCE`

De audience-claim die moet worden opgenomen in gegenereerde tokens en/of moet worden geverifieerd in gedecodeerde tokens.
Wanneer ingesteld op ``None``, wordt dit veld uitgesloten van het token en niet geverifieerd.

## `ISSUER`

De issuer-claim die moet worden opgenomen in gegenereerde tokens en/of moet worden geverifieerd in gedecodeerde tokens.
Wanneer ingesteld op ``None``, wordt dit veld uitgesloten van het token en niet geverifieerd.

### ``JWK_URL``
----------

De JWK_URL wordt gebruikt om de openbare sleutel die nodig is voor het verifiëren van token-handtekeningen dynamisch te resolveren.
Bij gebruik van Auth0 kun je dit bijvoorbeeld instellen op 'https://yourdomain.auth0.com/.well-known/jwks.json'.
Wanneer ingesteld op ``None``, wordt dit veld uitgesloten van de token-backend en niet gebruikt tijdens verificatie

### ``LEEWAY``
----------

Leeway wordt gebruikt om enige marge toe te staan bij de verlooptijd. Dit kan een geheel getal van seconden zijn of een ``datetime.timedelta``.
Raadpleeg https://pyjwt.readthedocs.io/en/latest/usage.html#expiration-time-claim-exp voor meer informatie.

###``AUTH_HEADER_TYPES``
---------------------

De type(s) autorisatieheader die worden geaccepteerd voor views die authenticatie vereisen. Een waarde van ``'Bearer'`` betekent bijvoorbeeld dat views die authenticatie vereisen zoeken naar een header met het volgende formaat:
``Authorization: Bearer <token>``. Deze instelling kan ook een lijst of tuple met mogelijke headertypes bevatten (bijv. ``('Bearer', 'JWT')``).
Als op deze manier een lijst of tuple wordt gebruikt en authenticatie mislukt, wordt het eerste item in de verzameling gebruikt om de header "WWW-Authenticate" in de response op te bouwen.

###``AUTH_HEADER_NAME``
----------------------------

De naam van de autorisatieheader die voor authenticatie wordt gebruikt. De standaardwaarde is `HTTP_AUTHORIZATION`, waarmee de header `Authorization` uit verzoeken wordt geaccepteerd.
Als je bijvoorbeeld `X_Access_Token` in je requestheaders wilt gebruiken, geef dan `AUTH_HEADER_NAME` op als `HTTP_X_ACCESS_TOKEN` in je instellingen.


###``USER_ID_FIELD``
-----------------

Het databaseveld in het gebruikersmodel dat wordt opgenomen in gegenereerde tokens om de gebruiker te identificeren.
Het wordt aanbevolen dat de waarde van deze instelling een veld specificeert dat doorgaans niet verandert zodra de beginwaarde is gekozen.
Het specificeren van een veld "username" of "email" zou bijvoorbeeld een slechte keuze zijn,
aangezien de username of het e-mailadres van een account kan veranderen, afhankelijk van hoe accountbeheer in een bepaalde service is ontworpen.
Dit zou het mogelijk kunnen maken dat een nieuw account wordt aangemaakt met een oude username, terwijl bestaande tokens die die username als gebruikersidentificatie gebruiken, geldig blijven.

###``USER_ID_CLAIM``
-----------------

De claim die wordt gebruikt om de gebruikersidentificatie op te slaan in gegenereerde tokens. Als de waarde bijvoorbeeld wordt ingesteld op ```"user_id"``` betekent dit dat het gegenereerde token een claim "user_id" bevat,
die de identificatie van de gebruiker bevat.

###``USER_AUTHENTICATION_RULE``
----------------------------

Een callable die wordt gebruikt om te bepalen of de gebruiker mag authenticeren. Deze regel wordt toegepast nadat een geldig token is verwerkt. Het gebruikersobject wordt als argument aan de callable doorgegeven.
De standaardregel controleert of de vlag ``is_active`` nog steeds ``True`` is.
De callable moet een booleaanse waarde retourneren, ``True`` betekent geautoriseerd, anders ``False`` wat resulteert in een 401-statuscode.

###``AUTH_TOKEN_CLASSES``
----------------------

Een lijst met gedoteerde paden die verwijzen naar klassen die de toegestane tokentypes specificeren om authenticatie aan te tonen. Meer informatie in de sectie "Token Types" hieronder.

###``TOKEN_TYPE_CLAIM``
--------------------

De naam van de claim die wordt gebruikt om het tokentype op te slaan. Meer informatie in de sectie "Token Types" hieronder.

###``JTI_CLAIM``
-------------

De naam van de claim die wordt gebruikt om de unieke identificatie van het token op te slaan. Deze identificatie wordt gebruikt om ingetrokken tokens te identificeren in de blacklist-app.
In sommige gevallen kan het nodig zijn om een andere claim dan de standaardclaim "jti" te gebruiken om zo'n waarde op te slaan.

###``TOKEN_USER_CLASS``
--------------------

Een stateless gebruikersobject dat wordt ondersteund door een geverifieerd token. Wordt alleen gebruikt door de authenticatiebackend JWTStatelessUser.
De waarde is een gedoteerd pad dat verwijst naar je subklasse van ``"rest_framework_simplejwt.models.TokenUser"``, wat ook de standaardwaarde is.

###``SLIDING_TOKEN_LIFETIME``
--------------------------

Een object ``datetime.timedelta`` dat specificeert hoe lang een sliding token geldig is om authenticatie aan te tonen.
Tijdens het genereren van tokens wordt deze ``timedelta``-waarde opgeteld bij de huidige UTC-tijd om de standaardclaimwaarde "exp" van het token te verkrijgen.
Meer informatie in de sectie "Sliding Tokens" hieronder.

###``SLIDING_TOKEN_REFRESH_LIFETIME``
----------------------------------

Een object ``datetime.timedelta`` dat specificeert hoe lang een sliding token geldig is om te worden vernieuwd.
Tijdens het genereren van tokens wordt deze `timedelta`-waarde opgeteld bij de huidige UTC-tijd om de standaardclaimwaarde "exp" van het token te verkrijgen.
Meer informatie in de sectie "Sliding Tokens" hieronder.

###``SLIDING_TOKEN_REFRESH_EXP_CLAIM``
-----------------------------------

De naam van de claim die wordt gebruikt om de verlooptijd van de refreshperiode van een sliding token op te slaan. Meer informatie in de sectie "Sliding Tokens" hieronder.

!!! success

    Ga verder naar het volgende hoofdstuk **[Token-claims Aanpassen](customizing_token_claims.md)**.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
