Title: 开始试用 Django Ninja


URL 来源：https://stackoverflow.com/questions/76531474/django-ninja-testing


[Django Ninja Testing](https://stackoverflow.com/questions/76531474/django-ninja-testing)
=========================================================================================

[提问](https://stackoverflow.com/questions/ask)


提问于 1 年前 1 个月

修改 4 个月前

浏览 2k 次

4

[](https://stackoverflow.com/posts/76531474/timeline "Show activity on this post.")


我正在尝试使用 Django-Ninja 为我编写的 API 创建一个测试。


这是我的模型：

    class Country(models.Model):
        created_at = models.DateTimeField(auto_created=True, auto_now_add=True)
        name = models.CharField(max_length=128, null=False, blank=False)
        code = models.CharField(max_length=128, null=False, blank=False, unique=True)
        timezone = models.CharField(max_length=128, null=False, blank=False)



这是我的方案：

    class CountryAddSchema(Schema):
        name: str
        code: str
        timezone: str



这是帖子的端点：

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



最后，这里是测试功能：

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



请注意，我在 `setUp` 中设置了 `self.AUTHORIZED_HEADER` 。


并且这里有个错误：

    FAIL: test_add_correct (address.tests_country.CountryTest)
    Add a country
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "SOME_PATH/tests_country.py", line 80, in test_add_correct
        self.assertEquals(respond.status_code, 201)
    AssertionError: 400 != 201



我可以使用 Django-Ninja 提供的 Swagger 添加一个国家。我的意思是端点有效。但我不能使用 `djano.test.Client` 进行测试。

Any Idea?

Update:
-------


这里是 swagger 生成的 curl 代码：

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




3 Answers 3
-----------


排序方式：重置为默认


最高分（默认） 热门（最近的投票更重要） 修改日期（最新的先） 创建日期（最早的先）

4

[](https://stackoverflow.com/posts/77486156/timeline "Show activity on this post.")


我有一个错误 `{"detail": "Cannot parse request body"}` 。


事实证明，Django-ninja 期望将数据作为 JSON 传递，但默认情况下，测试客户端将 `content_type` 设置为 `multipart/form-data; boundary=BoUnDaRyStRiNg` 。当您显式指定内容类型应为 JSON 时，它将起作用。

    Client().post(url, {"your": "dict"}, content_type="application/json")



注意：在头部设置内容类型将不起作用，因为它将被覆盖。

[Share](https://stackoverflow.com/a/77486156 "Short permalink to this answer")

[改进这个回答](https://stackoverflow.com/posts/77486156/edit)

Follow


已回答 2023 年 11 月 15 日 8 时 22 分

[![Image 3: Jorrick Sleijster's user avatar](https://i.sstatic.net/b3CbN.jpg?s=64)](https://stackoverflow.com/users/2277445/jorrick-sleijster)

[Jorrick Sleijster](https://stackoverflow.com/users/2277445/jorrick-sleijster)Jorrick Sleijster


109711 金徽章 1212 银徽章 2626 铜徽章

[Add a comment](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Use comments to ask for more information or suggest improvements. Avoid comments like “+1” or “thanks”.") |[](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Expand to show all comments on this post")

2

[](https://stackoverflow.com/posts/76651551/timeline "Show activity on this post.")


尝试将其转换为 JSON：

    self.client.post(
       reverse("api-1.0.0:address_country_add"),
       json.dumps(data),
       content_type="application/json", 
       **self.AUTHORIZED_HEADER
    )


[Share](https://stackoverflow.com/a/76651551 "Short permalink to this answer")

[改进这个回答](https://stackoverflow.com/posts/76651551/edit)

Follow


已回答，2023 年 7 月 10 日 7 时 26 分

[![Image 4: Djangonaut's user avatar](https://www.gravatar.com/avatar/d666ba0098fc4715697a4e54f088e89b?s=64&d=identicon&r=PG)](https://stackoverflow.com/users/208525/djangonaut)

[Djangonaut](https://stackoverflow.com/users/208525/djangonaut)Djangonaut

5,77177 gold badges4141 silver badges5555 bronze badges

2

* 我已经试过了。我找到解决方案了。我用了 `urllib.parse.urlencode` 。我会尽快把答案贴出来。

  – [MSH](https://stackoverflow.com/users/2681662/msh "2,209 reputation")


  已评论 2023 年 7 月 10 日 20:32

* 嗨嗨，能麻烦你把答案发一下吗？遇到了类似的问题

  – [Jorrick Sleijster](https://stackoverflow.com/users/2277445/jorrick-sleijster "1,097 reputation")


  评论于 2023 年 11 月 15 日 8:12

[Add a comment](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Use comments to ask for more information or suggest improvements. Avoid comments like “+1” or “thanks”.") |[](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Expand to show all comments on this post")

1

[](https://stackoverflow.com/posts/78178060/timeline "Show activity on this post.")


在使用 Django 测试客户端发送数据时，确保将其作为 JSON 数据发送，因为您的端点期望 JSON：

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
这应该符合你的 API 端点的预期，并解决 400 状态码问题。**

[Share](https://stackoverflow.com/a/78178060 "Short permalink to this answer")

[改进这个回答](https://stackoverflow.com/posts/78178060/edit)

Follow


已回答 3 月 18 日 5 时 11 分

[![Image 5: Nayem Jaman Tusher's user avatar](https://i.sstatic.net/IZuD9AWk.jpg?s=64)](https://stackoverflow.com/users/16545894/nayem-jaman-tusher)


纳伊姆·贾曼·图谢尔

97122 gold badges88 silver badges2222 bronze badges

[Add a comment](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Use comments to ask for more information or suggest improvements. Avoid comments like “+1” or “thanks”.") |[](https://stackoverflow.com/questions/76531474/django-ninja-testing# "Expand to show all comments on this post")


