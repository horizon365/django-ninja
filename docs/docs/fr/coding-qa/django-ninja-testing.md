Titre : Premiers pas avec Django Ninja


URL source : https://stackoverflow.com/questions/76531474/django-ninja-testing


[Test de Django Ninja](https://stackoverflow.com/questions/76531474/django-ninja-testing)
=========================================================================================

[Poser une question](https://stackoverflow.com/questions/ask)


Posée il y a 1 an et 1 mois

Modifiée il y a 4 mois

Consultée 2k fois

4

[](https://stackoverflow.com/posts/76531474/timeline "Show activity on this post.")


J'essaie de créer un test pour une API que j'ai écrite avec Django-Ninja.


Voici mon modèle :

    class Country(models.Model):
        created_at = models.DateTimeField(auto_created=True, auto_now_add=True)
        name = models.CharField(max_length=128, null=False, blank=False)
        code = models.CharField(max_length=128, null=False, blank=False, unique=True)
        timezone = models.CharField(max_length=128, null=False, blank=False)



Voici mon schéma :

    class CountryAddSchema(Schema):
        name: str
        code: str
        timezone: str



Voici l'endpoint du post :

    router.post("/add",
                 description="Add a Country",
                 summary="Add a Country", tags=["Address"],
                 response={201: DefaultSchema, 401: DefaultSchema, 422: DefaultSchema, 500: DefaultSchema},
                url_name="address_country_add")
    def country_add(request, country: CountryAddSchema):
        try:
            if not request.auth.belongs_to.is_staff:
                return 401, {"detail": "None Staff cannot add Country"}
    
            the_country = Country.objects.create(**country.dict())
            the_country.save()
            return 201, {"detail": "New Country created"}
        except Exception as e:
            return 500, {"detail": str(e)}



Enfin, voici la fonction de test :

    def test_add_correct(self):
        """
        Add a country
    
        """
        data = {
            "name": "".join(choices(ascii_letters, k=32)),
            "code": "".join(choices(ascii_letters, k=32)),
            "timezone": "".join(choices(ascii_letters, k=32))
        }
    
        respond = self.client.post(reverse("api-1.0.0:address_country_add"), data, **self.AUTHORIZED_HEADER)
        self.assertEquals(respond.status_code, 201)
        self.assertDictEqual(json.loads(respond.content), {"detail": "New Country created"})
    
        the_country = Country.objects.last()
        self.assertDictEqual(
            data,
            {
                "name": the_country.name,
                "code": the_country.code,
                "timezone": the_country.timezone
            }
        )



Notez que j'ai défini `self.AUTHORIZED_HEADER` dans `setUp`.


Et voici l'erreur :

    FAIL: test_add_correct (address.tests_country.CountryTest)
    Add a country
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "SOME_PATH/tests_country.py", line 80, in test_add_correct
        self.assertEquals(respond.status_code, 201)
    AssertionError: 400 != 201



Je peux ajouter un pays en utilisant le Swagger fourni par Django-Ninja. Je veux dire que l'endpoint fonctionne. Mais je ne peux pas le tester avec `djano.test.Client`.

Une idée ?

Mise à jour :
-------


Voici le code curl généré par swagger :

    curl -X 'POST' \
      'http://127.0.0.1:8000/api/address/country/add' \
      -H 'accept: application/json' \
      -H 'X-API-Key: API-KEY' \
      -H 'Content-Type: application/json' \
      -d '{
      "name": "string",
      "code": "string",
      "timezone": "string"
    }'




3 réponses 3
-----------


Trier par : Réinitialiser par défaut


Score le plus élevé (par défaut) Tendance (les votes récents comptent plus) Date de modification (plus récent d'abord) Date de création (plus ancien d'abord)

4

[](https://stackoverflow.com/posts/77486156/timeline "Show activity on this post.")


J'avais une erreur `{"detail": "Cannot parse request body"}` .


Il s'est avéré que Django-ninja s'attend à ce que les données soient passées en JSON, mais par défaut, le client de test définit `content_type` à `multipart/form-data; boundary=BoUnDaRyStRiNg`. Lorsque vous spécifiez explicitement que le type de contenu doit être JSON, cela fonctionne.

    Client().post(url, {"your": "dict"}, content_type="application/json")



Remarque : Définir le type de contenu dans les en-têtes ne fonctionnera pas car il sera écrasé.

[Partager](https://stackoverflow.com/a/77486156 "Short permalink to this answer")

[Améliorer cette réponse](https://stackoverflow.com/posts/77486156/edit)

Suivre


Répondu le 15 novembre 2023 à 8:22

[![Image 3: Jorrick Sleijster's user avatar](https://i.sstatic.net/b3CbN.jpg?s=64)](https://stackoverflow.com/users/2277445/jorrick-sleijster)

[Jorrick Sleijster](https://stackoverflow.com/users/2277445/jorrick-sleijster)Jorrick Sleijster


109711 gold badges1212 silver badges2626 bronze badges

[Ajouter un commentaire](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Use comments to ask for more information or suggest improvements. Avoid comments like “+1” or “thanks”.") |[](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Expand to show all comments on this post")

2

[](https://stackoverflow.com/posts/76651551/timeline "Show activity on this post.")


Essayez de le convertir en JSON :

    self.client.post(
       reverse("api-1.0.0:address_country_add"),
       json.dumps(data),
       content_type="application/json", 
       **self.AUTHORIZED_HEADER
    )



[Partager](https://stackoverflow.com/a/76651551 "Short permalink to this answer")

[Améliorer cette réponse](https://stackoverflow.com/posts/76651551/edit)

Suivre


Répondu le 10 juillet 2023 à 7:26

[![Image 4: Djangonaut's user avatar](https://www.gravatar.com/avatar/d666ba0098fc4715697a4e54f088e89b?s=64&d=identicon&r=PG)](https://stackoverflow.com/users/208525/djangonaut)

[Djangonaut](https://stackoverflow.com/users/208525/djangonaut)Djangonaut

5,77177 gold badges4141 silver badges5555 bronze badges

2

* J'ai essayé. J'ai trouvé une solution. J'ai utilisé `urllib.parse.urlencode`. Je publierai la réponse dès que possible.

  – [MSH](https://stackoverflow.com/users/2681662/msh "2,209 reputation")


  Commenté le 10 juillet 2023 à 20:32

* Bonjour, pourriez-vous s'il vous plaît publier votre réponse ? Je rencontre un problème similaire

  – [Jorrick Sleijster](https://stackoverflow.com/users/2277445/jorrick-sleijster "1,097 reputation")


  Commenté le 15 novembre 2023 à 8:12

[Ajouter un commentaire](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Use comments to ask for more information or suggest improvements. Avoid comments like “+1” or “thanks”.") |[](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Expand to show all comments on this post")

1

[](https://stackoverflow.com/posts/78178060/timeline "Show activity on this post.")


Lorsque vous envoyez des données avec le client de test Django, assurez-vous de les envoyer en tant que données JSON puisque votre endpoint attend du JSON :

    def test_add_correct(self):
        """
        Add  country
        """
        data = {
            "name": "".join(choices(ascii_letters, k=32)),
            "code": "".join(choices(ascii_letters, k=32)),
            "timezone": "".join(choices(ascii_letters, k=32))
        }
    
        # Convert data to JSON format
        data_json = json.dumps(data)
    
        # Send the request with JSON data
        respond = self.client.post(reverse("api-1.0.0:address_country_add"), data=data_json, content_type='application/json', **self.AUTHORIZED_HEADER)
    
        # Rest of your test code_____



**  
Cela devrait correspondre aux attentes de votre endpoint d'API et résoudre le problème du code d'état 400.**

[Partager](https://stackoverflow.com/a/78178060 "Short permalink to this answer")

[Améliorer cette réponse](https://stackoverflow.com/posts/78178060/edit)

Suivre


Répondu le 18 mars à 5:11

[![Image 5: Nayem Jaman Tusher's user avatar](https://i.sstatic.net/IZuD9AWk.jpg?s=64)](https://stackoverflow.com/users/16545894/nayem-jaman-tusher)


Nayem Jaman Tusher

97122 gold badges88 silver badges2222 bronze badges

[Ajouter un commentaire](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Use comments to ask for more information or suggest improvements. Avoid comments like “+1” or “thanks”.") |[](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Expand to show all comments on this post")
