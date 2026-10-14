# Djoser를 사용한 Django Ninja 토큰 인증


Source URL: https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser


중국어 콘텐츠: 이 질문은 리서치 노력을 보여줍니다; 유용하고 명확합니다

2

이 질문 저장하기.

[](https://stackoverflow.com/posts/70716976/timeline)


이 게시물의 활동 표시.


Django Ninja 프레임워크를 사용하여 CRUD를 구현했지만, 이제 애플리케이션에서 인증을 하고 싶습니다. Djoser를 설치하고 설정해서 이제 토큰을 생성할 수는 있지만, CRUD에서 토큰을 검증하는 방법을 모르겠습니다

    class AuthBearer(HttpBearer):
        def authenticate(self, request, token):
            if token == "supersecret":
                return token
    
    @api.get("/bearer", auth=AuthBearer())
    def bearer(request):
        return {"token": request.auth}



"AuthBearer" 함수에서 토큰을 확인할 수 있어야 하는데, 방법을 모르겠습니다

제 저장소 ([링크](https://github.com/arsalanses/ham-radio-logger/blob/master/logs/api/v1.py))

*   [django](https://stackoverflow.com/questions/tagged/django "show questions tagged 'django'")
*   [django-rest-framework](https://stackoverflow.com/questions/tagged/django-rest-framework "show questions tagged 'django-rest-framework'")
*   [djoser](https://stackoverflow.com/questions/tagged/djoser "show questions tagged 'djoser'")
*   [django-ninja](https://stackoverflow.com/questions/tagged/django-ninja "show questions tagged 'django-ninja'")

[공유](https://stackoverflow.com/q/70716976 "Short permalink to this question")


이 질문에 대한 링크 공유

링크 복사[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/ "The current license for this post: CC BY-SA 4.0")

[이 질문 개선하기](https://stackoverflow.com/posts/70716976/edit)

팔로우


이 질문을 팔로우하여 알림 받기

[2022년 12월 8일 17:18에 편집됨](https://stackoverflow.com/posts/70716976/revisions "show all edits to this post")

[![Image 1: metersk's user avatar](https://www.gravatar.com/avatar/f1a23a45808b0429be1543ca726d522f?s=64&d=identicon&r=PG)](https://stackoverflow.com/users/1887261/metersk)

[metersk](https://stackoverflow.com/users/1887261/metersk)

12.3k2222 골드 배지6868 실버 배지103103 브론즈 배지


2022년 1월 14일 21:59에 질문됨

[![Image 2: Arsalan's user avatar](https://i.sstatic.net/R9DYa.jpg?s=64)](https://stackoverflow.com/users/3711191/arsalan)

[Arsalan](https://stackoverflow.com/users/3711191/arsalan)Arsalan

7722 실버 배지99 브론즈 배지

[댓글 달기](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Use comments to ask for more information or suggest improvements. Avoid answering questions in comments.") |[](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Expand to show all comments on this post")

답변 1개
----------


정렬 기준: 기본값으로 재설정


최고 점수 (기본값) 트렌딩 (최근 투표 가중치 높음) 수정 날짜 (최신순) 작성 날짜 (오래된순)


이 답변이 유용합니다

6

답변 저장하기.

[](https://stackoverflow.com/posts/70720995/timeline)


이 게시물의 활동 표시.


기본적으로 Ninja의 HttpBearer 클래스를 확장하고 authenticate 메서드를 구현해야 합니다. 이 메서드는 request와 token을 인수로 받습니다. 이 메서드는 사용자가 인증되지 않은 경우 None을 반환하고, 인증된 경우 request.auth에 채워질 문자열을 반환합니다. 일반적으로 이 문자열은 사용자 이름이므로 모든 엔드포인트에서 사용할 수 있습니다. 다음과 같이 합니다 (토큰 디코딩에는 PyJWT를 사용합니다):

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


[공유](https://stackoverflow.com/a/70720995 "Short permalink to this answer")


이 답변에 대한 링크 공유

링크 복사[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/ "The current license for this post: CC BY-SA 4.0")

[이 답변 개선하기](https://stackoverflow.com/posts/70720995/edit)

팔로우


이 답변을 팔로우하여 알림 받기


2022년 1월 15일 오전 11:30에 답변됨

[![Image 3: abolfazlmalekahmadi's user avatar](https://i.sstatic.net/CeWmU.png?s=64)](https://stackoverflow.com/users/10356618/abolfazlmalekahmadi)

[abolfazlmalekahmadi](https://stackoverflow.com/users/10356618/abolfazlmalekahmadi)abolfazlmalekahmadi

26822 실버 배지1717 브론즈 배지

1

* 이 코드 예제 감사합니다! 인코딩된 토큰은 어떻게 생성하나요? 이 토큰들을 스토리지에 저장하나요?

  –[netcyrax](https://stackoverflow.com/users/2456568/netcyrax "1,089 reputation")

  [  
  2023년 7월 18일 9:29에 댓글 작성됨](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser#comment135243481_70720995)

[댓글 달기](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Use comments to ask for more information or suggest improvements. Avoid comments like “+1” or “thanks”.") |[](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Expand to show all comments on this post")

@media (prefers-color-scheme: dark) { body { color: #fff !important; background-color: #272727 !important; } } body { overflow-y: hidden; }
