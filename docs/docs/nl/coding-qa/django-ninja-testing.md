Title: Aan de slag met Django Ninja


Source URL: https://stackoverflow.com/questions/76531474/django-ninja-testing


[Testen met Django Ninja](https://stackoverflow.com/questions/76531474/django-ninja-testing)
=========================================================================================

[Stel een vraag](https://stackoverflow.com/questions/ask)


Gesteld 1 jaar, 1 maand geleden

Bewerkt 4 maanden geleden

2k keer bekeken

4

[](https://stackoverflow.com/posts/76531474/timeline "Show activity on this post.")


Ik probeer een test te maken voor een API die ik heb geschreven met Django-Ninja.


Hier is mijn model:

    class Country(models.Model):
        created_at = models.DateTimeField(auto_created=True, auto_now_add=True)
        name = models.CharField(max_length=128, null=False, blank=False)
        code = models.CharField(max_length=128, null=False, blank=False, unique=True)
        timezone = models.CharField(max_length=128, null=False, blank=False)



Hier is mijn schema:

    class CountryAddSchema(Schema):
        name: str
        code: str
        timezone: str



Hier is het endpoint van de post:

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



Ten slotte, hier is de testfunctie:

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



Merk op dat ik `self.AUTHORIZED_HEADER` heb ingesteld in `setUp`.


En hier is de foutmelding:

    FAIL: test_add_correct (address.tests_country.CountryTest)
    Add a country
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "SOME_PATH/tests_country.py", line 80, in test_add_correct
        self.assertEquals(respond.status_code, 201)
    AssertionError: 400 != 201



Ik kan een land toevoegen via de Swagger die Django-Ninja biedt. Ik bedoel: het endpoint werkt. Maar ik kan het niet testen met `djano.test.Client`.

Iemand een idee?

Update:
-------


Hier is de curl-code gegenereerd door swagger:

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



3 antwoorden 3
-----------


Sorteren op: Terugzetten naar standaard


Hoogste score (standaard) Trendend (recente stemmen tellen zwaarder) Datum gewijzigd (nieuwste eerst) Datum aangemaakt (oudste eerst)

4

[](https://stackoverflow.com/posts/77486156/timeline "Show activity on this post.")


Ik kreeg de foutmelding `{"detail": "Cannot parse request body"}` .


Het bleek dat Django-ninja verwacht dat de gegevens als JSON worden doorgegeven, maar dat de testclient standaard `content_type` instelt op `multipart/form-data; boundary=BoUnDaRyStRiNg`. Als je expliciet opgeeft dat het contenttype JSON moet zijn, werkt het.

    Client().post(url, {"your": "dict"}, content_type="application/json")



Let op: het contenttype in de headers zetten werkt niet, omdat het wordt overschreven.

[Delen](https://stackoverflow.com/a/77486156 "Short permalink to this answer")

[Verbeter dit antwoord](https://stackoverflow.com/posts/77486156/edit)

Volgen


Beantwoord op 15 nov. 2023 om 8:22

[![Image 3: Jorrick Sleijster's user avatar](https://i.sstatic.net/b3CbN.jpg?s=64)](https://stackoverflow.com/users/2277445/jorrick-sleijster)

[Jorrick Sleijster](https://stackoverflow.com/users/2277445/jorrick-sleijster)Jorrick Sleijster


109711 gouden badges1212 zilveren badges2626 bronzen badges

[Een reactie toevoegen](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Use comments to ask for more information or suggest improvements. Avoid comments like “+1” or “thanks”.") |[](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Expand to show all comments on this post")

2

[](https://stackoverflow.com/posts/76651551/timeline "Show activity on this post.")


Probeer het naar JSON te converteren:

    self.client.post(
       reverse("api-1.0.0:address_country_add"),
       json.dumps(data),
       content_type="application/json", 
       **self.AUTHORIZED_HEADER
    )



[Delen](https://stackoverflow.com/a/76651551 "Short permalink to this answer")

[Verbeter dit antwoord](https://stackoverflow.com/posts/76651551/edit)

Volgen


Beantwoord op 10 jul. 2023 om 7:26

[![Image 4: Djangonaut's user avatar](https://www.gravatar.com/avatar/d666ba0098fc4715697a4e54f088e89b?s=64&d=identicon&r=PG)](https://stackoverflow.com/users/208525/djangonaut)

[Djangonaut](https://stackoverflow.com/users/208525/djangonaut)Djangonaut

5,77177 gouden badges4141 zilveren badges5555 bronzen badges

2

* Ik heb het geprobeerd. Ik heb een oplossing gevonden. Ik gebruikte `urllib.parse.urlencode`. Ik plaats het antwoord zo snel mogelijk.

  – [MSH](https://stackoverflow.com/users/2681662/msh "2,209 reputation")


  Gereageerd op 10 jul. 2023 om 20:32

* Hoi, kun je je antwoord alsjeblieft plaatsen? Ik loop tegen een vergelijkbaar probleem aan

  – [Jorrick Sleijster](https://stackoverflow.com/users/2277445/jorrick-sleijster "1,097 reputation")


  Gereageerd op 15 nov. 2023 om 8:12

[Een reactie toevoegen](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Use comments to ask for more information or suggest improvements. Avoid comments like “+1” or “thanks”.") |[](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Expand to show all comments on this post")

1

[](https://stackoverflow.com/posts/78178060/timeline "Show activity on this post.")


Stuur bij het verzenden van gegevens met de Django-testclient de gegevens als JSON, aangezien je endpoint JSON verwacht:

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
Dit zou moeten aansluiten bij de verwachtingen van je API-endpoint en het probleem met de 400-statuscode oplossen.**

[Delen](https://stackoverflow.com/a/78178060 "Short permalink to this answer")

[Verbeter dit antwoord](https://stackoverflow.com/posts/78178060/edit)

Volgen


Beantwoord op 18 mrt. om 5:11

[![Image 5: Nayem Jaman Tusher's user avatar](https://i.sstatic.net/IZuD9AWk.jpg?s=64)](https://stackoverflow.com/users/16545894/nayem-jaman-tusher)


Nayem Jaman Tusher

97122 gouden badges88 zilveren badges2222 bronzen badges

[Een reactie toevoegen](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Use comments to ask for more information or suggest improvements. Avoid comments like “+1” or “thanks”.") |[](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Expand to show all comments on this post")
