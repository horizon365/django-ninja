Title: Django Ninja 入門


Source URL: https://stackoverflow.com/questions/76531474/django-ninja-testing


[Django Ninja Testing](https://stackoverflow.com/questions/76531474/django-ninja-testing)
=========================================================================================

[質問を投稿する](https://stackoverflow.com/questions/ask)


質問されたのは 1 年 1 か月前

更新は 4 か月前

閲覧数 2k 回

4

[](https://stackoverflow.com/posts/76531474/timeline "Show activity on this post.")


Django-Ninja で書いた API のテストを作成しようとしています。


以下が私のモデルです：

    class Country(models.Model):
        created_at = models.DateTimeField(auto_created=True, auto_now_add=True)
        name = models.CharField(max_length=128, null=False, blank=False)
        code = models.CharField(max_length=128, null=False, blank=False, unique=True)
        timezone = models.CharField(max_length=128, null=False, blank=False)



以下が私の schema です：

    class CountryAddSchema(Schema):
        name: str
        code: str
        timezone: str



以下が post のエンドポイントです：

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



最後に、以下がテスト関数です：

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



なお、`self.AUTHORIZED_HEADER` は `setUp` 内で設定しています。


そして、以下がエラーです：

    FAIL: test_add_correct (address.tests_country.CountryTest)
    Add a country
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "SOME_PATH/tests_country.py", line 80, in test_add_correct
        self.assertEquals(respond.status_code, 201)
    AssertionError: 400 != 201



Django-Ninja が提供する Swagger を使えば country を追加できます。つまりエンドポイント自体は動作しています。しかし `djano.test.Client` を使ってテストすることができません。

何かアイデアはありますか？
更新：
-------


以下は swagger が生成した curl コードです：

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




3 件の回答 3
-----------


並び順: デフォルトにリセット


スコアが高い順（デフォルト） トレンド（最近の投票がより多くカウントされる） 更新日順（新しいものが先） 作成日順（古いものが先）

4

[](https://stackoverflow.com/posts/77486156/timeline "Show activity on this post.")


私も `{"detail": "Cannot parse request body"}` というエラーに遭遇しました。


原因がわかったところでは、Django-ninja はデータが JSON として渡されることを期待していますが、デフォルトではテストクライアントが `content_type` を `multipart/form-data; boundary=BoUnDaRyStRiNg` に設定します。content type が JSON であることを明示的に指定すると、動作します。

    Client().post(url, {"your": "dict"}, content_type="application/json")



注意：ヘッダー内で content type を設定しても、上書きされるため機能しません。

[共有](https://stackoverflow.com/a/77486156 "Short permalink to this answer")

[この回答を改善する](https://stackoverflow.com/posts/77486156/edit)

フォロー


回答日時：2023 年 11 月 15 日 8:22

[![Image 3: Jorrick Sleijster's user avatar](https://i.sstatic.net/b3CbN.jpg?s=64)](https://stackoverflow.com/users/2277445/jorrick-sleijster)

[Jorrick Sleijster](https://stackoverflow.com/users/2277445/jorrick-sleijster)Jorrick Sleijster


109711 金バッジ1212 銀バッジ2626 銅バッジ

[コメントを追加](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Use comments to ask for more information or suggest improvements. Avoid comments like “+1” or “thanks”.") |[](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Expand to show all comments on this post")

2

[](https://stackoverflow.com/posts/76651551/timeline "Show activity on this post.")


JSON に変換してみてください：

    self.client.post(
       reverse("api-1.0.0:address_country_add"),
       json.dumps(data),
       content_type="application/json", 
       **self.AUTHORIZED_HEADER
    )



[共有](https://stackoverflow.com/a/76651551 "Short permalink to this answer")

[この回答を改善する](https://stackoverflow.com/posts/76651551/edit)

フォロー


回答日時：2023 年 7 月 10 日 7:26

[![Image 4: Djangonaut's user avatar](https://www.gravatar.com/avatar/d666ba0098fc4715697a4e54f088e89b?s=64&d=identicon&r=PG)](https://stackoverflow.com/users/208525/djangonaut)

[Djangonaut](https://stackoverflow.com/users/208525/djangonaut)Djangonaut

5,77177 金バッジ4141 銀バッジ5555 銅バッジ

2

* 試してみました。解決策が見つかりました。`urllib.parse.urlencode` を使いました。できるだけ早く回答を投稿します。

  – [MSH](https://stackoverflow.com/users/2681662/msh "2,209 reputation")


  コメント日時：2023 年 7 月 10 日 20:32

* こんにちは、回答を投稿していただけませんか？私も同様の問題に直面しています

  – [Jorrick Sleijster](https://stackoverflow.com/users/2277445/jorrick-sleijster "1,097 reputation")


  コメント日時：2023 年 11 月 15 日 8:12

[コメントを追加](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Use comments to ask for more information or suggest improvements. Avoid comments like “+1” or “thanks”.") |[](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Expand to show all comments on this post")

1

[](https://stackoverflow.com/posts/78178060/timeline "Show activity on this post.")


Django テストクライアントでデータを送信するときは、エンドポイントが JSON を期待しているため、JSON データとして送信するようにしてください：

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
これで API エンドポイントの期待に一致し、400 ステータスコードの問題が解決されるはずです。**

[共有](https://stackoverflow.com/a/78178060 "Short permalink to this answer")

[この回答を改善する](https://stackoverflow.com/posts/78178060/edit)

フォロー


回答日時：3 月 18 日 5:11

[![Image 5: Nayem Jaman Tusher's user avatar](https://i.sstatic.net/IZuD9AWk.jpg?s=64)](https://stackoverflow.com/users/16545894/nayem-jaman-tusher)


Nayem Jaman Tusher

97122 金バッジ88 銀バッジ2222 銅バッジ

[コメントを追加](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Use comments to ask for more information or suggest improvements. Avoid comments like “+1” or “thanks”.") |[](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Expand to show all comments on this post")
