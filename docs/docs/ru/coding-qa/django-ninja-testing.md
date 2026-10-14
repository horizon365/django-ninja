Заголовок: Начало работы с Django Ninja


Источник: https://stackoverflow.com/questions/76531474/django-ninja-testing


[Тестирование в Django Ninja](https://stackoverflow.com/questions/76531474/django-ninja-testing)
=========================================================================================

[Задать вопрос](https://stackoverflow.com/questions/ask)


Задан 1 год 1 месяц назад

Изменён 4 месяца назад

Просмотрен 2k раз

4

[](https://stackoverflow.com/posts/76531474/timeline "Show activity on this post.")


Я пытаюсь создать тест для API, которое написал с использованием Django-Ninja.


Вот моя модель:

    class Country(models.Model):
        created_at = models.DateTimeField(auto_created=True, auto_now_add=True)
        name = models.CharField(max_length=128, null=False, blank=False)
        code = models.CharField(max_length=128, null=False, blank=False, unique=True)
        timezone = models.CharField(max_length=128, null=False, blank=False)



Вот моя схема:

    class CountryAddSchema(Schema):
        name: str
        code: str
        timezone: str



Вот эндпоинт post:

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



Наконец, вот функция теста:

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



Обратите внимание, что я задаю `self.AUTHORIZED_HEADER` в `setUp`.


А вот ошибка:

    FAIL: test_add_correct (address.tests_country.CountryTest)
    Add a country
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "SOME_PATH/tests_country.py", line 80, in test_add_correct
        self.assertEquals(respond.status_code, 201)
    AssertionError: 400 != 201



Я могу добавить страну с помощью Swagger, предоставляемого Django-Ninja. То есть эндпоинт работает. Но я не могу протестировать его с помощью `djano.test.Client`.

Есть какие-нибудь идеи?

Обновление:
-------


Вот код curl, сгенерированный swagger:

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




3 ответа 3
-----------


Сортировка: Сброс на значение по умолчанию


Наивысший балл (по умолчанию) Актуальные (недавние голоса весят больше) По дате изменения (сначала новые) По дате создания (сначала новые)

4

[](https://stackoverflow.com/posts/77486156/timeline "Show activity on this post.")


У меня была ошибка `{"detail": "Cannot parse request body"}` .


Оказалось, что Django-ninja ожидает, что данные будут переданы как JSON, но по умолчанию тестовый клиент устанавливает `content_type` в `multipart/form-data; boundary=BoUnDaRyStRiNg`. Когда вы явно указываете, что тип содержимого должен быть JSON, всё работает.

    Client().post(url, {"your": "dict"}, content_type="application/json")



Примечание: установка типа содержимого в заголовках не сработает, поскольку он будет переопределён.

[Поделиться](https://stackoverflow.com/a/77486156 "Short permalink to this answer")

[Улучшить этот ответ](https://stackoverflow.com/posts/77486156/edit)

Подписаться


Ответ дан 15 ноября 2023 г. в 8:22

[![Image 3: Jorrick Sleijster's user avatar](https://i.sstatic.net/b3CbN.jpg?s=64)](https://stackoverflow.com/users/2277445/jorrick-sleijster)

[Jorrick Sleijster](https://stackoverflow.com/users/2277445/jorrick-sleijster)Jorrick Sleijster


109711 золотых знаков1212 серебряных знаков2626 бронзовых знаков

[Добавить комментарий](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Use comments to ask for more information or suggest improvements. Avoid comments like “+1” or “thanks”.") |[](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Expand to show all comments on this post")

2

[](https://stackoverflow.com/posts/76651551/timeline "Show activity on this post.")


Попробуйте преобразовать данные в JSON:

    self.client.post(
       reverse("api-1.0.0:address_country_add"),
       json.dumps(data),
       content_type="application/json", 
       **self.AUTHORIZED_HEADER
    )



[Поделиться](https://stackoverflow.com/a/76651551 "Short permalink to this answer")

[Улучшить этот ответ](https://stackoverflow.com/posts/76651551/edit)

Подписаться


Ответ дан 10 июля 2023 г. в 7:26

[![Image 4: Djangonaut's user avatar](https://www.gravatar.com/avatar/d666ba0098fc4715697a4e54f088e89b?s=64&d=identicon&r=PG)](https://stackoverflow.com/users/208525/djangonaut)

[Djangonaut](https://stackoverflow.com/users/208525/djangonaut)Djangonaut

5,77177 золотых знаков4141 серебряный знак5555 бронзовых знаков

2

* Я попробовал это. Я нашёл решение. Я использовал `urllib.parse.urlencode`. Скоро опубликую ответ.

  – [MSH](https://stackoverflow.com/users/2681662/msh "2,209 reputation")


  Комментарий дан 10 июля 2023 г. в 20:32

* Привет, не могли бы вы опубликовать свой ответ? Я столкнулся с похожей проблемой

  – [Jorrick Sleijster](https://stackoverflow.com/users/2277445/jorrick-sleijster "1,097 reputation")


  Комментарий дан 15 ноября 2023 г. в 8:12

[Добавить комментарий](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Use comments to ask for more information or suggest improvements. Avoid comments like “+1” or “thanks”.") |[](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Expand to show all comments on this post")

1

[](https://stackoverflow.com/posts/78178060/timeline "Show activity on this post.")


При отправке данных с помощью тестового клиента Django убедитесь, что вы отправляете их как JSON, поскольку ваш эндпоинт ожидает JSON:

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
Это должно соответствовать ожиданиям вашего эндпоинта API и решить проблему со статус-кодом 400.**

[Поделиться](https://stackoverflow.com/a/78178060 "Short permalink to this answer")

[Улучшить этот ответ](https://stackoverflow.com/posts/78178060/edit)

Подписаться


Ответ дан 18 марта в 5:11

[![Image 5: Nayem Jaman Tusher's user avatar](https://i.sstatic.net/IZuD9AWk.jpg?s=64)](https://stackoverflow.com/users/16545894/nayem-jaman-tusher)


Nayem Jaman Tusher

97122 золотых знака88 серебряных знаков2222 бронзовых знака

[Добавить комментарий](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Use comments to ask for more information or suggest improvements. Avoid comments like “+1” or “thanks”.") |[](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Expand to show all comments on this post")
