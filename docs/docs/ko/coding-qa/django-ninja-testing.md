Title: Django Ninja 시작하기


Source URL: https://stackoverflow.com/questions/76531474/django-ninja-testing


[Django Ninja 테스팅](https://stackoverflow.com/questions/76531474/django-ninja-testing)
=========================================================================================

[질문하기](https://stackoverflow.com/questions/ask)


1년 1개월 전에 질문됨

4개월 전에 수정됨

2천 회 조회됨

4

[](https://stackoverflow.com/posts/76531474/timeline "Show activity on this post.")


Django-Ninja를 사용하여 작성한 API에 대한 테스트를 만들려고 합니다.


다음은 제 모델입니다:

    class Country(models.Model):
        created_at = models.DateTimeField(auto_created=True, auto_now_add=True)
        name = models.CharField(max_length=128, null=False, blank=False)
        code = models.CharField(max_length=128, null=False, blank=False, unique=True)
        timezone = models.CharField(max_length=128, null=False, blank=False)



다음은 제 스키마입니다:

    class CountryAddSchema(Schema):
        name: str
        code: str
        timezone: str



다음은 post 엔드포인트입니다:

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



마지막으로 다음은 테스트 함수입니다:

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



`self.AUTHORIZED_HEADER`는 `setUp`에서 설정했습니다.


그리고 다음은 오류입니다:

    FAIL: test_add_correct (address.tests_country.CountryTest)
    Add a country
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "SOME_PATH/tests_country.py", line 80, in test_add_correct
        self.assertEquals(respond.status_code, 201)
    AssertionError: 400 != 201



Django-Ninja가 제공하는 Swagger를 사용하여 국가를 추가할 수 있습니다. 즉, 엔드포인트는 동작합니다. 하지만 `djano.test.Client`를 사용하여 테스트할 수 없습니다.

무슨 아이디어 없을까요?

업데이트:
-------


다음은 swagger가 생성한 curl 코드입니다:

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




답변 3개
-----------


정렬 기준: 기본값으로 재설정


최고 점수 (기본값) 트렌딩 (최근 투표 가중치 높음) 수정 날짜 (최신순) 작성 날짜 (오래된순)

4

[](https://stackoverflow.com/posts/77486156/timeline "Show activity on this post.")


`{"detail": "Cannot parse request body"}` 오류가 발생했습니다.


알고 보니 Django-ninja는 데이터가 JSON으로 전달되기를 기대하지만, 기본적으로 테스트 클라이언트는 `content_type`을 `multipart/form-data; boundary=BoUnDaRyStRiNg`으로 설정합니다. content type이 JSON이어야 함을 명시적으로 지정하면 작동합니다.

    Client().post(url, {"your": "dict"}, content_type="application/json")



참고: 헤더에 content type을 설정하는 것은 덮어쓰여지기 때문에 작동하지 않습니다.

[공유](https://stackoverflow.com/a/77486156 "Short permalink to this answer")

[이 답변 개선하기](https://stackoverflow.com/posts/77486156/edit)

팔로우


2023년 11월 15일 8:22에 답변됨

[![Image 3: Jorrick Sleijster's user avatar](https://i.sstatic.net/b3CbN.jpg?s=64)](https://stackoverflow.com/users/2277445/jorrick-sleijster)

[Jorrick Sleijster](https://stackoverflow.com/users/2277445/jorrick-sleijster)Jorrick Sleijster


109711 골드 배지1212 실버 배지2626 브론즈 배지

[댓글 달기](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Use comments to ask for more information or suggest improvements. Avoid comments like “+1” or “thanks”.") |[](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Expand to show all comments on this post")

2

[](https://stackoverflow.com/posts/76651551/timeline "Show activity on this post.")


JSON으로 변환해 보세요:

    self.client.post(
       reverse("api-1.0.0:address_country_add"),
       json.dumps(data),
       content_type="application/json", 
       **self.AUTHORIZED_HEADER
    )


[공유](https://stackoverflow.com/a/76651551 "Short permalink to this answer")

[이 답변 개선하기](https://stackoverflow.com/posts/76651551/edit)

팔로우


2023년 7월 10일 7:26에 답변됨

[![Image 4: Djangonaut's user avatar](https://www.gravatar.com/avatar/d666ba0098fc4715697a4e54f088e89b?s=64&d=identicon&r=PG)](https://stackoverflow.com/users/208525/djangonaut)

[Djangonaut](https://stackoverflow.com/users/208525/djangonaut)Djangonaut

5,77177 골드 배지4141 실버 배지5555 브론즈 배지

2

* 시도해 봤습니다. 해결책을 찾았습니다. `urllib.parse.urlencode`를 사용했습니다. 가능한 한 빨리 답변을 게시하겠습니다.

  – [MSH](https://stackoverflow.com/users/2681662/msh "2,209 reputation")


  2023년 7월 10일 20:32에 댓글 작성됨

* 안녕하세요, 답변을 게시해 주실 수 있나요? 저도 비슷한 문제를 겪고 있습니다

  – [Jorrick Sleijster](https://stackoverflow.com/users/2277445/jorrick-sleijster "1,097 reputation")


  2023년 11월 15일 8:12에 댓글 작성됨

[댓글 달기](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Use comments to ask for more information or suggest improvements. Avoid comments like “+1” or “thanks”.") |[](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Expand to show all comments on this post")

1

[](https://stackoverflow.com/posts/78178060/timeline "Show activity on this post.")


Django 테스트 클라이언트로 데이터를 보낼 때, 엔드포인트가 JSON을 기대하므로 JSON 데이터로 보내야 합니다:

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
이렇게 하면 API 엔드포인트의 기대치와 일치하여 400 상태 코드 문제를 해결할 수 있습니다.**

[공유](https://stackoverflow.com/a/78178060 "Short permalink to this answer")

[이 답변 개선하기](https://stackoverflow.com/posts/78178060/edit)

팔로우


3월 18일 5:11에 답변됨

[![Image 5: Nayem Jaman Tusher's user avatar](https://i.sstatic.net/IZuD9AWk.jpg?s=64)](https://stackoverflow.com/users/16545894/nayem-jaman-tusher)


Nayem Jaman Tusher

97122 골드 배지88 실버 배지2222 브론즈 배지

[댓글 달기](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Use comments to ask for more information or suggest improvements. Avoid comments like “+1” or “thanks”.") |[](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Expand to show all comments on this post")
