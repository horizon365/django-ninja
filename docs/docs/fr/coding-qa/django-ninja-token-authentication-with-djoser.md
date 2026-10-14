# Authentification par jeton Django Ninja avec Djoser


URL source : https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser


Contenu chinois : Cette question montre un effort de recherche ; elle est utile et claire

2

Enregistrez cette question.

[](https://stackoverflow.com/posts/70716976/timeline)


Afficher l'activité de ce post.


J'ai implémenté le CRUD en utilisant le framework Django Ninja, mais maintenant je veux m'authentifier dans mon application. J'ai installé et configuré Djoser, donc maintenant je peux générer des jetons, mais je ne sais pas comment les vérifier dans mon CRUD

    class AuthBearer(HttpBearer):
        def authenticate(self, request, token):
            if token == "supersecret":
                return token
    
    @api.get("/bearer", auth=AuthBearer())
    def bearer(request):
        return {"token": request.auth}



Je devrais être capable de vérifier le jeton dans la fonction « AuthBearer », mais je ne sais pas comment

mon dépôt ([lien](https://github.com/arsalanses/ham-radio-logger/blob/master/logs/api/v1.py))

*   [django](https://stackoverflow.com/questions/tagged/django "show questions tagged 'django'")
*   [django-rest-framework](https://stackoverflow.com/questions/tagged/django-rest-framework "show questions tagged 'django-rest-framework'")
*   [djoser](https://stackoverflow.com/questions/tagged/djoser "show questions tagged 'djoser'")
*   [django-ninja](https://stackoverflow.com/questions/tagged/django-ninja "show questions tagged 'django-ninja'")

[Partager](https://stackoverflow.com/q/70716976 "Short permalink to this question")


Partager un lien vers cette question

Copier le lien[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/ "The current license for this post: CC BY-SA 4.0")

[Améliorer cette question](https://stackoverflow.com/posts/70716976/edit)

Suivre


Suivre cette question pour recevoir des notifications

[modifié le 8 décembre 2022 à 17:18](https://stackoverflow.com/posts/70716976/revisions "show all edits to this post")

[![Image 1: metersk's user avatar](https://www.gravatar.com/avatar/f1a23a45808b0429be1543ca726d522f?s=64&d=identicon&r=PG)](https://stackoverflow.com/users/1887261/metersk)

[metersk](https://stackoverflow.com/users/1887261/metersk)

12.3k2222 gold badges6868 silver badges103103 bronze badges


Posée le 14 janvier 2022 à 21:59

[![Image 2: Arsalan's user avatar](https://i.sstatic.net/R9DYa.jpg?s=64)](https://stackoverflow.com/users/3711191/arsalan)

[Arsalan](https://stackoverflow.com/users/3711191/arsalan)Arsalan

7722 silver badges99 bronze badges

[Ajouter un commentaire](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Use comments to ask for more information or suggest improvements. Avoid answering questions in comments.") |[](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Expand to show all comments on this post")

1 réponse 1
----------


Trier par : Réinitialiser par défaut


Score le plus élevé (par défaut) Tendance (les votes récents comptent plus) Date de modification (plus récent d'abord) Date de création (plus ancien d'abord)


Cette réponse est utile

6

Enregistrez la réponse.

[](https://stackoverflow.com/posts/70720995/timeline)


Afficher l'activité de ce post.


Donc, en gros, vous devez étendre la classe HttpBearer de Ninja et implémenter la méthode authenticate, qui acceptera la requête et le jeton comme arguments. Cette méthode renverra None si l'utilisateur n'est pas authentifié, ou une chaîne qui sera peuplée dans request.auth si l'utilisateur est authentifié. Typiquement, cette chaîne sera le nom d'utilisateur, afin que vous puissiez l'utiliser dans tous les endpoints. Quelque chose comme ceci (j'utilise PyJWT pour décoder le jeton) :

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



[Partager](https://stackoverflow.com/a/70720995 "Short permalink to this answer")


Partager un lien vers cette réponse

Copier le lien[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/ "The current license for this post: CC BY-SA 4.0")

[Améliorer cette réponse](https://stackoverflow.com/posts/70720995/edit)

Suivre


Suivre cette réponse pour recevoir des notifications


Répondu le 15 janvier 2022 à 11:30 AM

[![Image 3: abolfazlmalekahmadi's user avatar](https://i.sstatic.net/CeWmU.png?s=64)](https://stackoverflow.com/users/10356618/abolfazlmalekahmadi)

[abolfazlmalekahmadi](https://stackoverflow.com/users/10356618/abolfazlmalekahmadi)abolfazlmalekahmadi

26822 silver badges1717 bronze badges

1

* Merci pour cet exemple de code ! Comment générez-vous le jeton encodé ? Stockez-vous ces jetons dans un stockage ?

  –[netcyrax](https://stackoverflow.com/users/2456568/netcyrax "1,089 reputation")

  [  
  Commenté le 18 juillet 2023 à 9:29](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser#comment135243481_70720995)

[Ajouter un commentaire](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Use comments to ask for more information or suggest improvements. Avoid comments like “+1” or “thanks”.") |[](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Expand to show all comments on this post")

@media (prefers-color-scheme: dark) { body { color: #fff !important; background-color: #272727 !important; } } body { overflow-y: hidden; }
