# 使用 djoser 进行 Django ninja 令牌身份验证


URL 来源：https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser


中文内容：这个问题显示了研究工作；它是有用且清晰的

2

保存此问题。

[](https://stackoverflow.com/posts/70716976/timeline)


显示此帖的活动。


我已经使用 Django Ninja 框架实现了 CRUD，但现在我希望在我的应用程序中进行认证。我已经安装并配置了 Djoser，因此现在我可以生成令牌，但我不知道如何在我的 CRUD 中进行验证

    class AuthBearer(HttpBearer):
        def authenticate(self, request, token):
            if token == "supersecret":
                return token
    
    @api.get("/bearer", auth=AuthBearer())
    def bearer(request):
        return {"token": request.auth}



我应该能够在“AuthBearer”函数中检查令牌，但我不知道如何做

my repo ([link](https://github.com/arsalanses/ham-radio-logger/blob/master/logs/api/v1.py))

*   [django](https://stackoverflow.com/questions/tagged/django "show questions tagged 'django'")
*   [django-rest-framework](https://stackoverflow.com/questions/tagged/django-rest-framework "show questions tagged 'django-rest-framework'")
*   [djoser](https://stackoverflow.com/questions/tagged/djoser "show questions tagged 'djoser'")
*   [django-ninja](https://stackoverflow.com/questions/tagged/django-ninja "show questions tagged 'django-ninja'")

[Share](https://stackoverflow.com/q/70716976 "Short permalink to this question")


分享这个问题的链接

Copy link[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/ "The current license for this post: CC BY-SA 4.0")

[改进这个问题](https://stackoverflow.com/posts/70716976/edit)

Follow


关注此问题以接收通知

[edited Dec 8, 2022 at 17:18](https://stackoverflow.com/posts/70716976/revisions "show all edits to this post")

[![Image 1: metersk's user avatar](https://www.gravatar.com/avatar/f1a23a45808b0429be1543ca726d522f?s=64&d=identicon&r=PG)](https://stackoverflow.com/users/1887261/metersk)

[metersk](https://stackoverflow.com/users/1887261/metersk)

12.3k2222 gold badges6868 silver badges103103 bronze badges


提问于 2022 年 1 月 14 日 21 点 59 分

[![Image 2: Arsalan's user avatar](https://i.sstatic.net/R9DYa.jpg?s=64)](https://stackoverflow.com/users/3711191/arsalan)

[Arsalan](https://stackoverflow.com/users/3711191/arsalan)Arsalan

7722 silver badges99 bronze badges

[Add a comment](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Use comments to ask for more information or suggest improvements. Avoid answering questions in comments.") |[](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Expand to show all comments on this post")

1 Answer 1
----------


排序方式：重置为默认


最高分（默认） 热门（最近的投票更重要） 修改日期（最新的先） 创建日期（最早的先）


这个答案有用

6

保存答案。

[](https://stackoverflow.com/posts/70720995/timeline)


显示此帖的活动。


所以基本上你必须扩展 Ninja 的 HttpBearer 类并实现 authenticate 方法，该方法将接受请求和令牌作为参数。如果用户未经过身份验证，此方法将返回 None，如果用户经过身份验证，则返回将在 request.auth 中填充的字符串。通常，此字符串将是用户名，因此你可以在所有端点中使用它。类似这样（我正在使用 PyJWT 进行令牌解码）：

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


[Share](https://stackoverflow.com/a/70720995 "Short permalink to this answer")


分享这个答案的链接

Copy link[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/ "The current license for this post: CC BY-SA 4.0")

[改进这个回答](https://stackoverflow.com/posts/70720995/edit)

Follow


按照此回答进行操作，即可接收通知


已回答，2022 年 1 月 15 日，上午 11:30

[![Image 3: abolfazlmalekahmadi's user avatar](https://i.sstatic.net/CeWmU.png?s=64)](https://stackoverflow.com/users/10356618/abolfazlmalekahmadi)

[abolfazlmalekahmadi](https://stackoverflow.com/users/10356618/abolfazlmalekahmadi)abolfazlmalekahmadi

26822 silver badges1717 bronze badges

1

* 谢谢这段代码示例！你是如何生成编码后的令牌的呢？你会将这些令牌存储在存储中吗？

  –[netcyrax](https://stackoverflow.com/users/2456568/netcyrax "1,089 reputation")

  [  
  有评论于 2023 年 7 月 18 日 9:29 发表](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser#comment135243481_70720995)

[Add a comment](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Use comments to ask for more information or suggest improvements. Avoid comments like “+1” or “thanks”.") |[](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Expand to show all comments on this post")

@media (prefers-color-scheme: dark) { body { color: #fff !important; background-color: #272727 !important; } } body { overflow-y: hidden; }