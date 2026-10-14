Title: Memulai dengan Django Ninja


Source URL: https://stackoverflow.com/questions/76531474/django-ninja-testing


[Testing Django Ninja](https://stackoverflow.com/questions/76531474/django-ninja-testing)
=========================================================================================

[Buat pertanyaan](https://stackoverflow.com/questions/ask)


Ditanyakan 1 tahun, 1 bulan yang lalu

Dimodifikasi 4 bulan yang lalu

Dilihat 2k kali

4

[](https://stackoverflow.com/posts/76531474/timeline "Show activity on this post.")


Saya sedang mencoba membuat test untuk sebuah API yang saya tulis menggunakan Django-Ninja.


Berikut model saya:

    class Country(models.Model):
        created_at = models.DateTimeField(auto_created=True, auto_now_add=True)
        name = models.CharField(max_length=128, null=False, blank=False)
        code = models.CharField(max_length=128, null=False, blank=False, unique=True)
        timezone = models.CharField(max_length=128, null=False, blank=False)



Berikut schema saya:

    class CountryAddSchema(Schema):
        name: str
        code: str
        timezone: str



Berikut endpoint dari post:

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



Terakhir, berikut fungsi test-nya:

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



Perhatikan bahwa saya mengatur `self.AUTHORIZED_HEADER` di `setUp`.


Dan berikut error-nya:

    FAIL: test_add_correct (address.tests_country.CountryTest)
    Add a country
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "SOME_PATH/tests_country.py", line 80, in test_add_correct
        self.assertEquals(respond.status_code, 201)
    AssertionError: 400 != 201



Saya bisa menambahkan sebuah country menggunakan Swagger yang disediakan Django-Ninja. Maksud saya, endpoint-nya berfungsi. Tetapi saya tidak bisa mengujinya menggunakan `djano.test.Client`.


Ada Ide?

Update:
-------


Berikut kode curl yang dihasilkan swagger:

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




3 Jawaban 3
-----------


Urutkan: Reset ke default


Skor tertinggi (default) Trending (vote terbaru dihitung lebih banyak) Tanggal dimodifikasi (terbaru dulu) Tanggal dibuat (terbaru dulu)

4

[](https://stackoverflow.com/posts/77486156/timeline "Show activity on this post.")


Saya mendapat error `{"detail": "Cannot parse request body"}` .


Ternyata Django-ninja mengharapkan data dikirimkan sebagai JSON, tetapi secara default test client mengatur `content_type` menjadi `multipart/form-data; boundary=BoUnDaRyStRiNg`. Ketika Anda secara eksplisit menentukan bahwa content type harusnya JSON, ini akan berfungsi.

    Client().post(url, {"your": "dict"}, content_type="application/json")


Catatan: Mengatur content type di headers tidak akan berfungsi karena nilainya akan ditimpa.

[Bagikan](https://stackoverflow.com/a/77486156 "Short permalink to this answer")

[Perbaiki jawaban ini](https://stackoverflow.com/posts/77486156/edit)

Follow


Dijawab Nov 15, 2023 pukul 8:22

[![Image 3: Jorrick Sleijster's user avatar](https://i.sstatic.net/b3CbN.jpg?s=64)](https://stackoverflow.com/users/2277445/jorrick-sleijster)

[Jorrick Sleijster](https://stackoverflow.com/users/2277445/jorrick-sleijster)Jorrick Sleijster


109711 gold badges1212 silver badges2626 bronze badges

[Tambahkan komentar](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Use comments to ask for more information or suggest improvements. Avoid comments like “+1” or “thanks”.") |[](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Expand to show all comments on this post")

2

[](https://stackoverflow.com/posts/76651551/timeline "Show activity on this post.")


Coba konversikan menjadi JSON:

    self.client.post(
       reverse("api-1.0.0:address_country_add"),
       json.dumps(data),
       content_type="application/json", 
       **self.AUTHORIZED_HEADER
    )


[Bagikan](https://stackoverflow.com/a/76651551 "Short permalink to this answer")

[Perbaiki jawaban ini](https://stackoverflow.com/posts/76651551/edit)

Follow


Dijawab Jul 10, 2023 pukul 7:26

[![Image 4: Djangonaut's user avatar](https://www.gravatar.com/avatar/d666ba0098fc4715697a4e54f088e89b?s=64&d=identicon&r=PG)](https://stackoverflow.com/users/208525/djangonaut)

[Djangonaut](https://stackoverflow.com/users/208525/djangonaut)Djangonaut

5,77177 gold badges4141 silver badges5555 bronze badges

2

* Saya sudah mencobanya. Saya menemukan sebuah solusi. Saya menggunakan `urllib.parse.urlencode`. Saya akan memposting jawaban secepatnya.

  – [MSH](https://stackoverflow.com/users/2681662/msh "2,209 reputation")


  Dikomentari Jul 10, 2023 pukul 20:32

* Hai, bisakah Anda memposting jawaban Anda? Saya menghadapi masalah serupa

  – [Jorrick Sleijster](https://stackoverflow.com/users/2277445/jorrick-sleijster "1,097 reputation")


  Dikomentari Nov 15, 2023 pukul 8:12

[Tambahkan komentar](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Use comments to ask for more information or suggest improvements. Avoid comments like “+1” or “thanks”.") |[](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Expand to show all comments on this post")

1

[](https://stackoverflow.com/posts/78178060/timeline "Show activity on this post.")


Saat mengirim data dengan Django test client, pastikan untuk mengirimkannya sebagai data JSON karena endpoint Anda mengharapkan JSON:

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
Ini seharusnya sesuai dengan ekspektasi endpoint API Anda dan menyelesaikan masalah status code 400.**

[Bagikan](https://stackoverflow.com/a/78178060 "Short permalink to this answer")

[Perbaiki jawaban ini](https://stackoverflow.com/posts/78178060/edit)

Follow


Dijawab Mar 18 pukul 5:11

[![Image 5: Nayem Jaman Tusher's user avatar](https://i.sstatic.net/IZuD9AWk.jpg?s=64)](https://stackoverflow.com/users/16545894/nayem-jaman-tusher)


Nayem Jaman Tusher

97122 gold badges88 silver badges2222 bronze badges

[Tambahkan komentar](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Use comments to ask for more information or suggest improvements. Avoid comments like “+1” or “thanks”.") |[](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Expand to show all comments on this post")
