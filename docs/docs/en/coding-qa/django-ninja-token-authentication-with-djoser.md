# Django Ninja Token Authentication with Djoser


Source URL: https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser


Chinese content: This question shows research effort; it is useful and clear

2

Save this question.

[](https://stackoverflow.com/posts/70716976/timeline)


Show activity on this post.


I have implemented CRUD using the Django Ninja framework, but now I want to authenticate in my application. I have installed and configured Djoser, so now I can generate tokens, but I don't know how to verify them in my CRUD

    class AuthBearer(HttpBearer):
        def authenticate(self, request, token):
            if token == "supersecret":
                return token
    
    @api.get("/bearer", auth=AuthBearer())
    def bearer(request):
        return {"token": request.auth}



I should be able to check the token in the "AuthBearer" function, but I don't know how

my repo ([link](https://github.com/arsalanses/ham-radio-logger/blob/master/logs/api/v1.py))

*   [django](https://stackoverflow.com/questions/tagged/django "show questions tagged 'django'")
*   [django-rest-framework](https://stackoverflow.com/questions/tagged/django-rest-framework "show questions tagged 'django-rest-framework'")
*   [djoser](https://stackoverflow.com/questions/tagged/djoser "show questions tagged 'djoser'")
*   [django-ninja](https://stackoverflow.com/questions/tagged/django-ninja "show questions tagged 'django-ninja'")

[Share](https://stackoverflow.com/q/70716976 "Short permalink to this question")


Share a link to this question

Copy link[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/ "The current license for this post: CC BY-SA 4.0")

[Improve this question](https://stackoverflow.com/posts/70716976/edit)

Follow


Follow this question to receive notifications

[edited Dec 8, 2022 at 17:18](https://stackoverflow.com/posts/70716976/revisions "show all edits to this post")

[![Image 1: metersk's user avatar](https://www.gravatar.com/avatar/f1a23a45808b0429be1543ca726d522f?s=64&d=identicon&r=PG)](https://stackoverflow.com/users/1887261/metersk)

[metersk](https://stackoverflow.com/users/1887261/metersk)

12.3k2222 gold badges6868 silver badges103103 bronze badges


Asked Jan 14, 2022 at 21:59

[![Image 2: Arsalan's user avatar](https://i.sstatic.net/R9DYa.jpg?s=64)](https://stackoverflow.com/users/3711191/arsalan)

[Arsalan](https://stackoverflow.com/users/3711191/arsalan)Arsalan

7722 silver badges99 bronze badges

[Add a comment](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Use comments to ask for more information or suggest improvements. Avoid answering questions in comments.") |[](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Expand to show all comments on this post")

1 Answer 1
----------


Sort by: Reset to default


Highest score (default) Trending (recent votes count more) Date modified (newest first) Date created (oldest first)


This answer is useful

6

Save the answer.

[](https://stackoverflow.com/posts/70720995/timeline)


Show activity on this post.


So basically you have to extend Ninja's HttpBearer class and implement the authenticate method, which will accept the request and the token as arguments. This method will return None if the user is not authenticated, or a string that will be populated in request.auth if the user is authenticated. Typically, this string will be the username, so you can use it across all endpoints. Something like this (I am using PyJWT to decode the token):

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


Share a link to this answer

Copy link[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/ "The current license for this post: CC BY-SA 4.0")

[Improve this answer](https://stackoverflow.com/posts/70720995/edit)

Follow


Follow this answer to receive notifications


Answered Jan 15, 2022 at 11:30 AM

[![Image 3: abolfazlmalekahmadi's user avatar](https://i.sstatic.net/CeWmU.png?s=64)](https://stackoverflow.com/users/10356618/abolfazlmalekahmadi)

[abolfazlmalekahmadi](https://stackoverflow.com/users/10356618/abolfazlmalekahmadi)abolfazlmalekahmadi

26822 silver badges1717 bronze badges

1

* Thanks for this code example! How do you generate the encoded token? Do you store these tokens in storage?

  –[netcyrax](https://stackoverflow.com/users/2456568/netcyrax "1,089 reputation")

  [  
  Commented Jul 18, 2023 at 9:29](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser#comment135243481_70720995)

[Add a comment](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Use comments to ask for more information or suggest improvements. Avoid comments like “+1” or “thanks”.") |[](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Expand to show all comments on this post")

@media (prefers-color-scheme: dark) { body { color: #fff !important; background-color: #272727 !important; } } body { overflow-y: hidden; }
