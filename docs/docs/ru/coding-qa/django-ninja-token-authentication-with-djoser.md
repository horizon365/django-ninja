# Аутентификация по токену в Django Ninja с Djoser


Источник: https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser


Контент на китайском: этот вопрос показывает исследовательскую работу; он полезен и понятен

2

Сохраните этот вопрос.

[](https://stackoverflow.com/posts/70716976/timeline)


Показать активность по этому сообщению.


Я реализовал CRUD с использованием фреймворка Django Ninja, но теперь я хочу выполнить аутентификацию в своём приложении. Я установил и настроил Djoser, так что теперь я могу генерировать токены, но я не знаю, как проверять их в моём CRUD

    class AuthBearer(HttpBearer):
        def authenticate(self, request, token):
            if token == "supersecret":
                return token
    
    @api.get("/bearer", auth=AuthBearer())
    def bearer(request):
        return {"token": request.auth}



Я должен иметь возможность проверять токен в функции "AuthBearer", но я не знаю как

мой репозиторий ([ссылка](https://github.com/arsalanses/ham-radio-logger/blob/master/logs/api/v1.py))

*   [django](https://stackoverflow.com/questions/tagged/django "show questions tagged 'django'")
*   [django-rest-framework](https://stackoverflow.com/questions/tagged/django-rest-framework "show questions tagged 'django-rest-framework'")
*   [djoser](https://stackoverflow.com/questions/tagged/djoser "show questions tagged 'djoser'")
*   [django-ninja](https://stackoverflow.com/questions/tagged/django-ninja "show questions tagged 'django-ninja'")

[Поделиться](https://stackoverflow.com/q/70716976 "Short permalink to this question")


Поделиться ссылкой на этот вопрос

Копировать ссылку[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/ "The current license for this post: CC BY-SA 4.0")

[Улучшить этот вопрос](https://stackoverflow.com/posts/70716976/edit)

Подписаться


Подписаться на этот вопрос, чтобы получать уведомления

[изменён 8 дек. 2022 г. в 17:18](https://stackoverflow.com/posts/70716976/revisions "show all edits to this post")

[![Image 1: metersk's user avatar](https://www.gravatar.com/avatar/f1a23a45808b0429be1543ca726d522f?s=64&d=identicon&r=PG)](https://stackoverflow.com/users/1887261/metersk)

[metersk](https://stackoverflow.com/users/1887261/metersk)

12.3k2222 золотых знака6868 серебряных знаков103103 бронзовых знака


Задан 14 янв. 2022 г. в 21:59

[![Image 2: Arsalan's user avatar](https://i.sstatic.net/R9DYa.jpg?s=64)](https://stackoverflow.com/users/3711191/arsalan)

[Arsalan](https://stackoverflow.com/users/3711191/arsalan)Arsalan

7722 серебряных знака99 бронзовых знаков

[Добавить комментарий](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Use comments to ask for more information or suggest improvements. Avoid answering questions in comments.") |[](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Expand to show all comments on this post")

1 ответ 1
----------


Сортировка: Сброс на значение по умолчанию


Наивысший балл (по умолчанию) Актуальные (недавние голоса весят больше) По дате изменения (сначала новые) По дате создания (сначала новые)


Этот ответ полезен

6

Сохраните ответ.

[](https://stackoverflow.com/posts/70720995/timeline)


Показать активность по этому сообщению.


По сути, вам нужно расширить класс HttpBearer в Ninja и реализовать метод authenticate, который будет принимать request и token в качестве аргументов. Этот метод вернёт None, если пользователь не аутентифицирован, или строку, которая будет записана в request.auth, если пользователь аутентифицирован. Обычно этой строкой является имя пользователя, так что вы можете использовать её во всех эндпоинтах. Что-то вроде этого (я использую PyJWT для декодирования токена):

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



[Поделиться](https://stackoverflow.com/a/70720995 "Short permalink to this answer")


Поделиться ссылкой на этот ответ

Копировать ссылку[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/ "The current license for this post: CC BY-SA 4.0")

[Улучшить этот ответ](https://stackoverflow.com/posts/70720995/edit)

Подписаться


Подписаться на этот ответ, чтобы получать уведомления


Ответ дан 15 янв. 2022 г. в 11:30 AM

[![Image 3: abolfazlmalekahmadi's user avatar](https://i.sstatic.net/CeWmU.png?s=64)](https://stackoverflow.com/users/10356618/abolfazlmalekahmadi)

[abolfazlmalekahmadi](https://stackoverflow.com/users/10356618/abolfazlmalekahmadi)abolfazlmalekahmadi

26822 серебряных знака1717 бронзовых знаков

1

* Спасибо за этот пример кода! Как вы генерируете закодированный токен? Храните ли вы эти токены в хранилище?

  –[netcyrax](https://stackoverflow.com/users/2456568/netcyrax "1,089 reputation")

  [  
  Комментарий дан 18 июля 2023 г. в 9:29](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser#comment135243481_70720995)

[Добавить комментарий](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Use comments to ask for more information or suggest improvements. Avoid comments like “+1” or “thanks”.") |[](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Expand to show all comments on this post")

@media (prefers-color-scheme: dark) { body { color: #fff !important; background-color: #272727 !important; } } body { overflow-y: hidden; }
