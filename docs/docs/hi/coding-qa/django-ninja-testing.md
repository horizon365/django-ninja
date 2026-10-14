Title: Django Ninja के साथ शुरुआत


Source URL: https://stackoverflow.com/questions/76531474/django-ninja-testing


[Django Ninja Testing](https://stackoverflow.com/questions/76531474/django-ninja-testing)
=========================================================================================

[एक प्रश्न पूछें](https://stackoverflow.com/questions/ask)


1 वर्ष, 1 महीना पहले पूछा गया

4 महीने पहले संशोधित

2k बार देखा गया

4

[](https://stackoverflow.com/posts/76531474/timeline "Show activity on this post.")


मैं Django-Ninja का उपयोग करके लिखे गए एक API के लिए test बनाने की कोशिश कर रहा हूँ।


यहाँ मेरा model है:

    class Country(models.Model):
        created_at = models.DateTimeField(auto_created=True, auto_now_add=True)
        name = models.CharField(max_length=128, null=False, blank=False)
        code = models.CharField(max_length=128, null=False, blank=False, unique=True)
        timezone = models.CharField(max_length=128, null=False, blank=False)



यहाँ मेरा schema है:

    class CountryAddSchema(Schema):
        name: str
        code: str
        timezone: str



यहाँ post का endpoint है:

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



अंत में, यहाँ test function है:

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



ध्यान दें कि मैंने `self.AUTHORIZED_HEADER` को `setUp` में सेट किया है।


और यहाँ error है:

    FAIL: test_add_correct (address.tests_country.CountryTest)
    Add a country
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "SOME_PATH/tests_country.py", line 80, in test_add_correct
        self.assertEquals(respond.status_code, 201)
    AssertionError: 400 != 201



मैं Django-Ninja द्वारा प्रदान किए गए Swagger का उपयोग करके एक country जोड़ सकता हूँ। मेरा मतलब है कि endpoint काम करता है। लेकिन मैं `djano.test.Client` का उपयोग करके इसे test नहीं कर पा रहा।

कोई विचार?

Update:
-------


यहाँ swagger द्वारा generate किया गया curl कोड है:

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



3 उत्तर 3
-----------


Sort by: Reset to default


Highest score (default) Trending (recent votes count more) Date modified (newest first) Date created (oldest first)

4

[](https://stackoverflow.com/posts/77486156/timeline "Show activity on this post.")


मुझे एक error `{"detail": "Cannot parse request body"}` मिला।


पता चला कि Django-ninja अपेक्षा करता है कि data JSON के रूप में पास किया जाए, लेकिन डिफ़ॉल्ट रूप से test client `content_type` को `multipart/form-data; boundary=BoUnDaRyStRiNg` सेट करता है। जब आप स्पष्ट रूप से निर्दिष्ट करते हैं कि content type JSON होना चाहिए, तो यह काम करेगा।

    Client().post(url, {"your": "dict"}, content_type="application/json")


ध्यान दें: headers में content type सेट करना काम नहीं करेगा क्योंकि इसे override कर दिया जाएगा।

[Share](https://stackoverflow.com/a/77486156 "Short permalink to this answer")

[Improve this answer](https://stackoverflow.com/posts/77486156/edit)

Follow


Answered Nov 15, 2023 at 8:22

[![Image 3: Jorrick Sleijster's user avatar](https://i.sstatic.net/b3CbN.jpg?s=64)](https://stackoverflow.com/users/2277445/jorrick-sleijster)

[Jorrick Sleijster](https://stackoverflow.com/users/2277445/jorrick-sleijster)Jorrick Sleijster


109711 gold badges1212 silver badges2626 bronze badges

[Add a comment](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Use comments to ask for more information or suggest improvements. Avoid comments like “+1” or “thanks”.") |[](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Expand to show all comments on this post")

2

[](https://stackoverflow.com/posts/76651551/timeline "Show activity on this post.")


इसे JSON में बदलने की कोशिश करें:

    self.client.post(
       reverse("api-1.0.0:address_country_add"),
       json.dumps(data),
       content_type="application/json", 
       **self.AUTHORIZED_HEADER
    )


[Share](https://stackoverflow.com/a/76651551 "Short permalink to this answer")

[Improve this answer](https://stackoverflow.com/posts/76651551/edit)

Follow


Answered Jul 10, 2023 at 7:26

[![Image 4: Djangonaut's user avatar](https://www.gravatar.com/avatar/d666ba0098fc4715697a4e54f088e89b?s=64&d=identicon&r=PG)](https://stackoverflow.com/users/208525/djangonaut)

[Djangonaut](https://stackoverflow.com/users/208525/djangonaut)Djangonaut

5,77177 gold badges4141 silver badges5555 bronze badges

2

* मैंने इसे आज़माया है। मुझे एक solution मिला। मैंने `urllib.parse.urlencode` का उपयोग किया। मैं जितनी जल्दी हो सके उत्तर post करूँगा।

  – [MSH](https://stackoverflow.com/users/2681662/msh "2,209 reputation")


  Commented Jul 10, 2023 at 20:32

* नमस्ते, क्या आप कृपया अपना उत्तर post कर सकते हैं? मुझे एक समान समस्या का सामना करना पड़ रहा है

  – [Jorrick Sleijster](https://stackoverflow.com/users/2277445/jorrick-sleijster "1,097 reputation")


  Commented Nov 15, 2023 at 8:12

[Add a comment](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Use comments to ask for more information or suggest improvements. Avoid comments like “+1” or “thanks”.") |[](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Expand to show all comments on this post")

1

[](https://stackoverflow.com/posts/78178060/timeline "Show activity on this post.")


Django test client के साथ data भेजते समय, इसे JSON data के रूप में भेजना सुनिश्चित करें क्योंकि आपका endpoint JSON की अपेक्षा करता है:

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
यह आपके API endpoint की अपेक्षाओं से मेल खाना चाहिए और 400 status code की समस्या को हल करना चाहिए।**

[Share](https://stackoverflow.com/a/78178060 "Short permalink to this answer")

[Improve this answer](https://stackoverflow.com/posts/78178060/edit)

Follow


Answered Mar 18 at 5:11

[![Image 5: Nayem Jaman Tusher's user avatar](https://i.sstatic.net/IZuD9AWk.jpg?s=64)](https://stackoverflow.com/users/16545894/nayem-jaman-tusher)


Nayem Jaman Tusher

97122 gold badges88 silver badges2222 bronze badges

[Add a comment](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Use comments to ask for more information or suggest improvements. Avoid comments like “+1” or “thanks”.") |[](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Expand to show all comments on this post")
