# Django Ninja Token-Authentifizierung mit Djoser


Source URL: https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser


Inhalt auf Chinesisch: Diese Frage zeigt Rechercheaufwand; sie ist nützlich und klar

2

Diese Frage speichern.

[](https://stackoverflow.com/posts/70716976/timeline)


Aktivitäten zu diesem Beitrag anzeigen


Ich habe CRUD mit dem Django Ninja Framework implementiert, aber jetzt möchte ich mich in meiner Anwendung authentifizieren. Ich habe Djoser installiert und konfiguriert, sodass ich jetzt Tokens generieren kann, aber ich weiß nicht, wie ich sie in meinem CRUD verifizieren soll

    class AuthBearer(HttpBearer):
        def authenticate(self, request, token):
            if token == "supersecret":
                return token
    
    @api.get("/bearer", auth=AuthBearer())
    def bearer(request):
        return {"token": request.auth}



Eigentlich sollte ich den Token in der Funktion „AuthBearer" prüfen können, aber ich weiß nicht, wie

mein Repo ([Link](https://github.com/arsalanses/ham-radio-logger/blob/master/logs/api/v1.py))

*   [django](https://stackoverflow.com/questions/tagged/django "show questions tagged 'django'")
*   [django-rest-framework](https://stackoverflow.com/questions/tagged/django-rest-framework "show questions tagged 'django-rest-framework'")
*   [djoser](https://stackoverflow.com/questions/tagged/djoser "show questions tagged 'djoser'")
*   [django-ninja](https://stackoverflow.com/questions/tagged/django-ninja "show questions tagged 'django-ninja'")

[Teilen](https://stackoverflow.com/q/70716976 "Short permalink to this question")


Einen Link zu dieser Frage teilen

Link kopieren[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/ "The current license for this post: CC BY-SA 4.0")

[Diese Frage verbessern](https://stackoverflow.com/posts/70716976/edit)

Folgen


Folgen Sie dieser Frage, um Benachrichtigungen zu erhalten

[bearbeitet am 8. Dezember 2022 um 17:18](https://stackoverflow.com/posts/70716976/revisions "show all edits to this post")

[![Image 1: metersk's user avatar](https://www.gravatar.com/avatar/f1a23a45808b0429be1543ca726d522f?s=64&d=identicon&r=PG)](https://stackoverflow.com/users/1887261/metersk)

[metersk](https://stackoverflow.com/users/1887261/metersk)

12,3k2222 Gold-Badges6868 Silber-Badges103103 Bronze-Badges


Gestellt am 14. Januar 2022 um 21:59

[![Image 2: Arsalan's user avatar](https://i.sstatic.net/R9DYa.jpg?s=64)](https://stackoverflow.com/users/3711191/arsalan)

[Arsalan](https://stackoverflow.com/users/3711191/arsalan)Arsalan

7722 Silber-Badges99 Bronze-Badges

[Add a comment](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Use comments to ask for more information or suggest improvements. Avoid answering questions in comments.") |[](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Expand to show all comments on this post")

1 Antwort 1
----------


Sortieren nach: Auf Standard zurücksetzen


Höchste Punktzahl (Standard) Trending (aktuelle Bewertungen zählen mehr) Datum der Änderung (neueste zuerst) Datum der Erstellung (neueste zuerst)


Diese Antwort ist nützlich

6

Diese Antwort speichern.

[](https://stackoverflow.com/posts/70720995/timeline)


Aktivitäten zu diesem Beitrag anzeigen


Im Grunde müssen Sie die HttpBearer-Klasse von Ninja erweitern und die Methode `authenticate` implementieren, die den Request und den Token als Argumente entgegennimmt. Diese Methode gibt None zurück, wenn der Benutzer nicht authentifiziert ist, oder einen String, der in request.auth hinterlegt wird, wenn der Benutzer authentifiziert ist. Typischerweise ist dieser String der Benutzername, sodass Sie ihn in allen Endpunkten verwenden können. Etwa so (ich verwende PyJWT, um den Token zu dekodieren):

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


[Teilen](https://stackoverflow.com/a/70720995 "Short permalink to this answer")


Einen Link zu dieser Antwort teilen

Link kopieren[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/ "The current license for this post: CC BY-SA 4.0")

[Diese Antwort verbessern](https://stackoverflow.com/posts/70720995/edit)

Folgen


Folgen Sie dieser Antwort, um Benachrichtigungen zu erhalten


Beantwortet am 15. Januar 2022 um 11:30 AM

[![Image 3: abolfazlmalekahmadi's user avatar](https://i.sstatic.net/CeWmU.png?s=64)](https://stackoverflow.com/users/10356618/abolfazlmalekahmadi)

[abolfazlmalekahmadi](https://stackoverflow.com/users/10356618/abolfazlmalekahmadi)abolfazlmalekahmadi

26822 Silber-Badges1717 Bronze-Badges

1

* Danke für dieses Codebeispiel! Wie erzeugen Sie den kodierten Token? Speichern Sie diese Tokens in einem Speicher?

  –[netcyrax](https://stackoverflow.com/users/2456568/netcyrax "1,089 reputation")

  [  
  Kommentiert am 18. Juli 2023 um 9:29](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser#comment135243481_70720995)

[Add a comment](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Use comments to ask for more information or suggest improvements. Avoid comments like “+1” or “thanks”.") |[](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Expand to show all comments on this post")

@media (prefers-color-scheme: dark) { body { color: #fff !important; background-color: #272727 !important; } } body { overflow-y: hidden; }
