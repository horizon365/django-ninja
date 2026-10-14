# Django Ninja tokenauthenticatie met Djoser


Source URL: https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser


Chinese inhoud: Deze vraag toont onderzoeksinspanning; hij is nuttig en duidelijk

2

Bewaar deze vraag.

[](https://stackoverflow.com/posts/70716976/timeline)


Toon activiteit op deze post.


Ik heb CRUD geïmplementeerd met het Django Ninja-framework, maar nu wil ik authenticatie in mijn applicatie. Ik heb Djoser geïnstalleerd en geconfigureerd, dus ik kan nu tokens genereren, maar ik weet niet hoe ik ze in mijn CRUD moet verifiëren

    class AuthBearer(HttpBearer):
        def authenticate(self, request, token):
            if token == "supersecret":
                return token
    
    @api.get("/bearer", auth=AuthBearer())
    def bearer(request):
        return {"token": request.auth}



Ik zou het token moeten kunnen controleren in de functie "AuthBearer", maar ik weet niet hoe

mijn repo ([link](https://github.com/arsalanses/ham-radio-logger/blob/master/logs/api/v1.py))

*   [django](https://stackoverflow.com/questions/tagged/django "show questions tagged 'django'")
*   [django-rest-framework](https://stackoverflow.com/questions/tagged/django-rest-framework "show questions tagged 'django-rest-framework'")
*   [djoser](https://stackoverflow.com/questions/tagged/djoser "show questions tagged 'djoser'")
*   [django-ninja](https://stackoverflow.com/questions/tagged/django-ninja "show questions tagged 'django-ninja'")

[Delen](https://stackoverflow.com/q/70716976 "Short permalink to this question")


Deel een link naar deze vraag

Link kopiëren[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/ "The current license for this post: CC BY-SA 4.0")

[Verbeter deze vraag](https://stackoverflow.com/posts/70716976/edit)

Volgen


Volg deze vraag om meldingen te ontvangen

[bewerkt op 8 dec. 2022 om 17:18](https://stackoverflow.com/posts/70716976/revisions "show all edits to this post")

[![Image 1: metersk's user avatar](https://www.gravatar.com/avatar/f1a23a45808b0429be1543ca726d522f?s=64&d=identicon&r=PG)](https://stackoverflow.com/users/1887261/metersk)

[metersk](https://stackoverflow.com/users/1887261/metersk)

12.3k2222 gouden badges6868 zilveren badges103103 bronzen badges


Gesteld op 14 jan. 2022 om 21:59

[![Image 2: Arsalan's user avatar](https://i.sstatic.net/R9DYa.jpg?s=64)](https://stackoverflow.com/users/3711191/arsalan)

[Arsalan](https://stackoverflow.com/users/3711191/arsalan)Arsalan

7722 zilveren badges99 bronzen badges

[Een reactie toevoegen](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Use comments to ask for more information or suggest improvements. Avoid answering questions in comments.") |[](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Expand to show all comments on this post")

1 antwoord 1
----------


Sorteren op: Terugzetten naar standaard


Hoogste score (standaard) Trendend (recente stemmen tellen zwaarder) Datum gewijzigd (nieuwste eerst) Datum aangemaakt (oudste eerst)


Dit antwoord is nuttig

6

Bewaar het antwoord.

[](https://stackoverflow.com/posts/70720995/timeline)


Toon activiteit op deze post.


Eigenlijk moet je de HttpBearer-klasse van Ninja uitbreiden en de methode authenticate implementeren, die het request en het token als argumenten accepteert. Deze methode geeft None terug als de gebruiker niet is geauthenticeerd, of een string die in request.auth wordt gevuld als de gebruiker wél is geauthenticeerd. Meestal is deze string de gebruikersnaam, zodat je deze in alle endpoints kunt gebruiken. Zoiets als dit (ik gebruik PyJWT om het token te decoderen):

    import jwt
    from ninja.security import HttpBearer
    
    class AuthBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                #JWT secret key is set up in settings.py
                JWT_SIGNING_KEY = getattr(settings, "JWT_SIGNING_KEY", None)
                payload = jwt.decode(token, JWT_SIGNING_KEY, algorithms=["HS256"])
                username: str = payload.get("sub")
                if username is None:
                    return None
            except jwt.PyJWTError as e:
                return None
    
            return username



[Delen](https://stackoverflow.com/a/70720995 "Short permalink to this answer")


Deel een link naar dit antwoord

Link kopiëren[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/ "The current license for this post: CC BY-SA 4.0")

[Verbeter dit antwoord](https://stackoverflow.com/posts/70720995/edit)

Volgen


Volg dit antwoord om meldingen te ontvangen


Beantwoord op 15 jan. 2022 om 11:30

[![Image 3: abolfazlmalekahmadi's user avatar](https://i.sstatic.net/CeWmU.png?s=64)](https://stackoverflow.com/users/10356618/abolfazlmalekahmadi)

[abolfazlmalekahmadi](https://stackoverflow.com/users/10356618/abolfazlmalekahmadi)abolfazlmalekahmadi

26822 zilveren badges1717 bronzen badges

1

* Bedankt voor dit codevoorbeeld! Hoe genereer je het gecodeerde token? Sla je deze tokens op in een opslag?

  –[netcyrax](https://stackoverflow.com/users/2456568/netcyrax "1,089 reputation")

  [  
  Gereageerd op 18 jul. 2023 om 9:29](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser#comment135243481_70720995)

[Een reactie toevoegen](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Use comments to ask for more information or suggest improvements. Avoid comments like “+1” or “thanks”.") |[](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Expand to show all comments on this post")

@media (prefers-color-scheme: dark) { body { color: #fff !important; background-color: #272727 !important; } } body { overflow-y: hidden; }
