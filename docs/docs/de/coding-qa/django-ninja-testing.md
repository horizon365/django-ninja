Titel: Erste Schritte mit Django Ninja


Source URL: https://stackoverflow.com/questions/76531474/django-ninja-testing


[Django Ninja Testing](https://stackoverflow.com/questions/76531474/django-ninja-testing)
=========================================================================================

[Eine Frage stellen](https://stackoverflow.com/questions/ask)


Gestellt vor 1 Jahr, 1 Monat

Geändert vor 4 Monaten

2.000-mal angesehen

4

[](https://stackoverflow.com/posts/76531474/timeline "Show activity on this post.")


Ich versuche, einen Test für eine API zu erstellen, die ich mit Django-Ninja geschrieben habe.


Hier ist mein Modell:

    class Country(models.Model):
        created_at = models.DateTimeField(auto_created=True, auto_now_add=True)
        name = models.CharField(max_length=128, null=False, blank=False)
        code = models.CharField(max_length=128, null=False, blank=False, unique=True)
        timezone = models.CharField(max_length=128, null=False, blank=False)



Hier ist mein Schema:

    class CountryAddSchema(Schema):
        name: str
        code: str
        timezone: str



Hier ist der Endpunkt für den Post:

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



Und schließlich hier die Testfunktion:

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



Beachten Sie, dass ich `self.AUTHORIZED_HEADER` in `setUp` gesetzt habe.


Und hier ist der Fehler:

    FAIL: test_add_correct (address.tests_country.CountryTest)
    Add a country
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "SOME_PATH/tests_country.py", line 80, in test_add_correct
        self.assertEquals(respond.status_code, 201)
    AssertionError: 400 != 201



Ich kann ein Land über die von Django-Ninja bereitgestellte Swagger-Benutzeroberfläche hinzufügen. Ich meine, der Endpunkt funktioniert. Aber ich kann ihn nicht mit `djano.test.Client` testen.

Irgendwelche Ideen?

Update:
-------


Hier ist der curl-Code, der von Swagger generiert wurde:

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




3 Antworten 3
-----------


Sortieren nach: Auf Standard zurücksetzen


Höchste Punktzahl (Standard) Trending (aktuelle Bewertungen zählen mehr) Datum der Änderung (neueste zuerst) Datum der Erstellung (neueste zuerst)

4

[](https://stackoverflow.com/posts/77486156/timeline "Show activity on this post.")


Ich hatte den Fehler `{"detail": "Cannot parse request body"}` .


Es stellte sich heraus, dass Django-ninja erwartet, dass die Daten als JSON übergeben werden, aber standardmäßig setzt der Test-Client `content_type` auf `multipart/form-data; boundary=BoUnDaRyStRiNg`. Wenn Sie explizit angeben, dass der Content-Type JSON sein soll, funktioniert es.

    Client().post(url, {"your": "dict"}, content_type="application/json")


Hinweis: Das Setzen des Content-Types in den Headern funktioniert nicht, weil er überschrieben wird.

[Teilen](https://stackoverflow.com/a/77486156 "Short permalink to this answer")

[Diese Antwort verbessern](https://stackoverflow.com/posts/77486156/edit)

Folgen


Beantwortet am 15. November 2023 um 8:22

[![Image 3: Jorrick Sleijster's user avatar](https://i.sstatic.net/b3CbN.jpg?s=64)](https://stackoverflow.com/users/2277445/jorrick-sleijster)

[Jorrick Sleijster](https://stackoverflow.com/users/2277445/jorrick-sleijster)Jorrick Sleijster


109711 Gold-Badges1212 Silber-Badges2626 Bronze-Badges

[Add a comment](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Use comments to ask for more information or suggest improvements. Avoid comments like “+1” or “thanks”.") |[](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Expand to show all comments on this post")

2

[](https://stackoverflow.com/posts/76651551/timeline "Show activity on this post.")


Versuchen Sie, es in JSON umzuwandeln:

    self.client.post(
       reverse("api-1.0.0:address_country_add"),
       json.dumps(data),
       content_type="application/json", 
       **self.AUTHORIZED_HEADER
    )


[Teilen](https://stackoverflow.com/a/76651551 "Short permalink to this answer")

[Diese Antwort verbessern](https://stackoverflow.com/posts/76651551/edit)

Folgen


Beantwortet am 10. Juli 2023 um 7:26

[![Image 4: Djangonaut's user avatar](https://www.gravatar.com/avatar/d666ba0098fc4715697a4e54f088e89b?s=64&d=identicon&r=PG)](https://stackoverflow.com/users/208525/djangonaut)

[Djangonaut](https://stackoverflow.com/users/208525/djangonaut)Djangonaut

5,77177 Gold-Badges4141 Silber-Badges5555 Bronze-Badges

2

* Ich habe es ausprobiert. Ich habe eine Lösung gefunden. Ich habe `urllib.parse.urlencode` verwendet. Ich werde die Antwort so bald wie möglich posten.

  – [MSH](https://stackoverflow.com/users/2681662/msh "2,209 reputation")


  Kommentiert am 10. Juli 2023 um 20:32

* Hallo, könntest du bitte deine Antwort posten? Ich habe ein ähnliches Problem

  – [Jorrick Sleijster](https://stackoverflow.com/users/2277445/jorrick-sleijster "1,097 reputation")


  Kommentiert am 15. November 2023 um 8:12

[Add a comment](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Use comments to ask for more information or suggest improvements. Avoid comments like “+1” or “thanks”.") |[](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Expand to show all comments on this post")

1

[](https://stackoverflow.com/posts/78178060/timeline "Show activity on this post.")


Wenn Sie Daten mit dem Django-Test-Client senden, stellen Sie sicher, dass Sie sie als JSON-Daten senden, da Ihr Endpunkt JSON erwartet:

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
Das sollte den Erwartungen Ihres API-Endpunkts entsprechen und das Problem mit dem Statuscode 400 beheben.**

[Teilen](https://stackoverflow.com/a/78178060 "Short permalink to this answer")

[Diese Antwort verbessern](https://stackoverflow.com/posts/78178060/edit)

Folgen


Beantwortet am 18. März um 5:11

[![Image 5: Nayem Jaman Tusher's user avatar](https://i.sstatic.net/IZuD9AWk.jpg?s=64)](https://stackoverflow.com/users/16545894/nayem-jaman-tusher)


Nayem Jaman Tusher

97122 Gold-Badges88 Silber-Badges2222 Bronze-Badges

[Add a comment](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Use comments to ask for more information or suggest improvements. Avoid comments like “+1” or “thanks”.") |[](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Expand to show all comments on this post")

