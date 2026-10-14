# Djoser के साथ Django Ninja Token Authentication


Source URL: https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser


चीनी content: यह प्रश्न शोध प्रयास दर्शाता है; यह उपयोगी और स्पष्ट है

2

इस प्रश्न को सहेजें।

[](https://stackoverflow.com/posts/70716976/timeline)


इस post पर गतिविधि दिखाएं।


मैंने Django Ninja framework का उपयोग करके CRUD implement किया है, लेकिन अब मैं अपनी application में authenticate करना चाहता हूँ। मैंने Djoser install और configure कर लिया है, इसलिए अब मैं tokens generate कर सकता हूँ, लेकिन मुझे नहीं पता कि अपने CRUD में उन्हें कैसे सत्यापित करूँ

    class AuthBearer(HttpBearer):
        def authenticate(self, request, token):
            if token == "supersecret":
                return token
    
    @api.get("/bearer", auth=AuthBearer())
    def bearer(request):
        return {"token": request.auth}



मुझे "AuthBearer" function में token की जाँच करने में सक्षम होना चाहिए, लेकिन मुझे नहीं पता कि कैसे

मेरी repo ([link](https://github.com/arsalanses/ham-radio-logger/blob/master/logs/api/v1.py))

*   [django](https://stackoverflow.com/questions/tagged/django "show questions tagged 'django'")
*   [django-rest-framework](https://stackoverflow.com/questions/tagged/django-rest-framework "show questions tagged 'django-rest-framework'")
*   [djoser](https://stackoverflow.com/questions/tagged/djoser "show questions tagged 'djoser'")
*   [django-ninja](https://stackoverflow.com/questions/tagged/django-ninja "show questions tagged 'django-ninja'")

[Share](https://stackoverflow.com/q/70716976 "Short permalink to this question")


इस प्रश्न का एक link share करें

Copy link[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/ "The current license for this post: CC BY-SA 4.0")

[Improve this question](https://stackoverflow.com/posts/70716976/edit)

Follow


इस प्रश्न को follow करें ताकि notifications प्राप्त हो सकें

[edited Dec 8, 2022 at 17:18](https://stackoverflow.com/posts/70716976/revisions "show all edits to this post")

[![Image 1: metersk's user avatar](https://www.gravatar.com/avatar/f1a23a45808b0429be1543ca726d522f?s=64&d=identicon&r=PG)](https://stackoverflow.com/users/1887261/metersk)

[metersk](https://stackoverflow.com/users/1887261/metersk)

12.3k2222 gold badges6868 silver badges103103 bronze badges


Asked Jan 14, 2022 at 21:59

[![Image 2: Arsalan's user avatar](https://i.sstatic.net/R9DYa.jpg?s=64)](https://stackoverflow.com/users/3711191/arsalan)

[Arsalan](https://stackoverflow.com/users/3711191/arsalan)Arsalan

7722 silver badges99 bronze badges

[Add a comment](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Use comments to ask for more information or suggest improvements. Avoid answering questions in comments.") |[](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Expand to show all comments on this post")

1 उत्तर 1
----------


Sort by: Reset to default


Highest score (default) Trending (recent votes count more) Date modified (newest first) Date created (oldest first)


यह उत्तर उपयोगी है

6

उत्तर को सहेजें।

[](https://stackoverflow.com/posts/70720995/timeline)


इस post पर गतिविधि दिखाएं।


तो मूल रूप से आपको Ninja की HttpBearer class को extend करना होगा और authenticate method implement करना होगा, जो arguments के रूप में request और token स्वीकार करेगा। यदि user authenticated नहीं है तो यह method None return करेगा, या एक string return करेगा जो user के authenticated होने पर request.auth में populate होगी। आमतौर पर, यह string username होगी, ताकि आप इसे सभी endpoints में उपयोग कर सकें। कुछ इस तरह (मैं token decode करने के लिए PyJWT का उपयोग कर रहा हूँ):

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


इस उत्तर का एक link share करें

Copy link[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/ "The current license for this post: CC BY-SA 4.0")

[Improve this answer](https://stackoverflow.com/posts/70720995/edit)

Follow


इस उत्तर को follow करें ताकि notifications प्राप्त हो सकें


Answered Jan 15, 2022 at 11:30 AM

[![Image 3: abolfazlmalekahmadi's user avatar](https://i.sstatic.net/CeWmU.png?s=64)](https://stackoverflow.com/users/10356618/abolfazlmalekahmadi)

[abolfazlmalekahmadi](https://stackoverflow.com/users/10356618/abolfazlmalekahmadi)abolfazlmalekahmadi

26822 silver badges1717 bronze badges

1

* इस code example के लिए धन्यवाद! आप encoded token कैसे generate करते हैं? क्या आप इन tokens को storage में रखते हैं?

  –[netcyrax](https://stackoverflow.com/users/2456568/netcyrax "1,089 reputation")

  [  
  Commented Jul 18, 2023 at 9:29](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser#comment135243481_70720995)

[Add a comment](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Use comments to ask for more information or suggest improvements. Avoid comments like “+1” or “thanks”.") |[](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Expand to show all comments on this post")

@media (prefers-color-scheme: dark) { body { color: #fff !important; background-color: #272727 !important; } } body { overflow-y: hidden; }
