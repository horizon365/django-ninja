---
comments: true
---
# CSRF (межсайтовая подделка запроса)

## Что такое межсайтовая подделка запроса?
> [Межсайтовая подделка запроса](https://en.wikipedia.org/wiki/Cross-site_request_forgery) происходит, когда вредоносный веб-сайт содержит ссылку, кнопку формы или некоторый JavaScript-код, предназначенные для использования учётных данных вошедшего пользователя (который посещает вредоносный сайт в своём браузере) для выполнения каких-либо действий на вашем сайте (или в других местах, не охваченных этим документом).


## Как защититься от межсайтовой подделки запроса с помощью Django Ninja
### Используйте методы аутентификации, которые не встраиваются в запросы автоматически
Атаки межсайтовой подделки запроса полагаются на методы аутентификации, которые автоматически включаются в запросы, исходящие с других сайтов, например [cookies](https://en.wikipedia.org/wiki/HTTP_cookie) или [Basic access authentication](https://en.wikipedia.org/wiki/Basic_access_authentication).
Использование метода аутентификации, который не встраивается автоматически, например `Authorization: Bearer`, смягчает эту атаку.


### Используйте встроенную защиту Django от межсайтовой подделки запроса
Если вы используете стандартную аутентификацию Django, основанную на cookies, вы также должны использовать стандартную [защиту Django от межсайтовой подделки запроса](https://docs.djangoproject.com/en/4.2/ref/csrf/).


По умолчанию в **Django Ninja** защита от межсайтовой подделки запроса **ВЫКЛЮЧЕНА** для всех операций.
Чтобы включить её, нужно использовать аргумент `csrf` класса NinjaAPI:

```python hl_lines="3"
from ninja import NinjaAPI

api = NinjaAPI(csrf=True)
```

<span style="color: red;">Warning</span>: Использование аутентификации на основе cookies с выключенной защитой от межсайтовой подделки запроса небезопасно! (например, `CookieKey` или `django_auth`).


**Django Ninja** автоматически включит защиту от межсайтовой подделки запроса для аутентификации на основе cookies.


```python hl_lines="8"
from ninja import NinjaAPI
from ninja.security import APIKeyCookie

class CookieAuth(APIKeyCookie):
    def authenticate(self, request, key):
        return key == "test"

api = NinjaAPI(auth=CookieAuth())

```


Или на основе django-auth (который наследуется от аутентификации на основе cookies):

```python hl_lines="4"
from ninja import NinjaAPI
from ninja.security import django_auth

api = NinjaAPI(auth=django_auth)
```


#### Декоратор Django `ensure_csrf_cookie`
Вы можете использовать декоратор Django [ensure_csrf_cookie](https://docs.djangoproject.com/en/4.2/ref/csrf/#django.views.decorators.csrf.ensure_csrf_cookie) на незащищённом маршруте, чтобы он включал заголовок `Set-Cookie` с токеном защиты от межсайтовой подделки запроса. Обратите внимание:
- Декоратор маршрута должен выполняться раньше (то есть располагаться выше) декоратора [ensure_csrf_cookie](https://docs.djangoproject.com/en/4.2/ref/csrf/#django.views.decorators.csrf.ensure_csrf_cookie).
- Для этого маршрута нужно применить `csrf_exempt`.
- Декоратор `ensure_csrf_cookie` работает только с Django `HttpResponse`, а не со словарём, как это делают большинство декораторов Django Ninja.
```python hl_lines="4"
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

@api.post("/csrf")
@ensure_csrf_cookie
@csrf_exempt
def get_csrf_token(request):
    return HttpResponse()
```
Запрос к этому маршруту приведёт к ответу Django с соответствующим заголовком `Set-Cookie`.


#### Клиентский (front-end) код
Вы можете использовать разделы [Using CSRF protection with AJAX](https://docs.djangoproject.com/en/4.2/howto/csrf/#using-csrf-protection-with-ajax) и [Setting the token on the AJAX request](https://docs.djangoproject.com/en/4.2/howto/csrf/#setting-the-token-on-the-ajax-request) из документации [How to use Django's CSRF protection](https://docs.djangoproject.com/en/4.2/howto/csrf/), чтобы узнать, как обрабатывать токен защиты от межсайтовой подделки запроса в вашем клиентском коде.


## О CORS
Возможно, вы захотите разместить свой front-end и API на разных сайтах (в этом случае обратите внимание на [django-cors-headers](https://github.com/adamchainz/django-cors-headers)).
Хотя это не напрямую связано с межсайтовой подделкой запроса, CORS (Cross-Origin Resource Sharing) может быть полезен, когда вы определяете cookies для защиты от межсайтовой подделки запроса на другом сайте, отличном от сайта front-end, так как по умолчанию [same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy) этого не разрешает.
Затем вы можете обратиться к [django-cors-headers README](https://github.com/adamchainz/django-cors-headers#readme).

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
