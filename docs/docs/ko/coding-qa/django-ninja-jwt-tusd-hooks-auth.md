---
comments: true
---
다음은 Markdown 블로그에 적합한 기술 문서로, `django-ninja-jwt`를 사용하여 `tusd`의 HTTP Hooks와 통합하여 사용자 인증을 수행하는 방법을 소개합니다.

---

# django-ninja-jwt를 사용하여 tusd의 HTTP Hooks와 사용자 인증 통합하기

재개 가능 업로드를 지원하는 대용량 파일 업로드 서비스를 구축할 때 [`tusd`](https://github.com/tus/tusd)는 매우 인기 있는 서버 측 구현입니다. Django 프로젝트에서는 일반적으로 [django-ninja](https://django-ninja.dev) 프레임워크를 [django-ninja-jwt](https://pypi.org/project/django-ninja-jwt/)와 함께 사용하여 API 개발 및 인증을 수행합니다.

이 글에서는 **tusd의 HTTP Hooks**와 `django-ninja-jwt`를 결합하여 사용자 식별 및 업로드 권한 제어를 구현하는 방법을 소개합니다.

---

## 1. tusd의 HTTP Hooks 소개

`tusd`는 업로드 생명주기의 다양한 단계(예: `pre-create`, `post-finish`)에서 Hook을 트리거하는 것을 지원합니다. `--hooks-http` 파라미터를 설정하면 Hook이 트리거될 때 `tusd`가 HTTP 요청을 전송합니다.

설정 명령 예시:

```bash
tusd \
  -hooks-http http://localhost:8000/tusd-hook/ \
  -cors-allow-origin "http://localhost:8080" \
  -cors-allow-credentials \
  -upload-dir ./uploads
```

업로드 작업이 발생하면 tusd는 지정된 주소로 JSON 페이로드를 POST하며, 여기에는 요청 헤더(예: `Authorization` 또는 `Cookie`)와 업로드 메타데이터가 포함됩니다.

---

## 2. tus-js-client로 JWT 요청 헤더 설정하기

프론트엔드에서 `tus-js-client`를 사용하는 경우(예: Vue/Quasar 애플리케이션), 요청 헤더에 JWT 토큰을 첨부해야 합니다:

```js
import tus from 'tus-js-client'

const upload = new tus.Upload(file, {
  endpoint: 'http://localhost:1080/files/',
  metadata: {
    filename: file.name,
    filetype: file.type
  },
  headers: {
    Authorization: 'Bearer ' + localStorage.getItem('access_token') // JWT token
  },
  withCredentials: false, // Do not use cookies; use the Authorization header
  onError: (error) => console.error(error),
  onSuccess: () => console.log('Upload succeeded')
})

upload.start()
```

---

## 3. 백엔드: Django에서 tusd Hook을 수신하고 JWT 검증하기

Django 프로젝트에 Hook 수신 엔드포인트를 생성합니다:

```python
# views.py
from ninja import Router
from ninja_jwt.authentication import JWTAuth
from django.http import JsonResponse
from django.contrib.auth import get_user_model
import json

router = Router()

@router.post("/tusd-hook")
def tusd_hook(request):
    try:
        payload = json.loads(request.body)
        headers = payload.get("HTTPRequest", {}).get("Header", {})
        auth_header = headers.get("Authorization", [""])[0]

        if auth_header.startswith("Bearer "):
            token = auth_header.split("Bearer ")[1]

            # Use django-ninja-jwt's JWTAuth to parse the token
            user = JWTAuth().authenticate(request, token)

            if user is None:
                return JsonResponse({"error": "Invalid token"}, status=401)

            # user is an authenticated Django User instance
            print("Upload user:", user.username)

            # You can perform authorization or write to the database based on user info
            return JsonResponse({"status": "ok"})

        return JsonResponse({"error": "No token"}, status=401)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
```

---

## 4. 라우트 등록

```python
# urls.py
from django.urls import path
from ninja import NinjaAPI
from .views import router as tusd_router

api = NinjaAPI()
api.add_router("/", tusd_router)

urlpatterns = [
    path("tusd-hook/", api.urls),
]
```

---

## 5. tusd Hook 요청 예시 (POST)

tusd는 백엔드로 다음과 유사한 JSON을 전송합니다:

```json
{
  "Protocol": "http",
  "EventName": "pre-create",
  "Upload": {
    "ID": "123456",
    "Size": 1024000,
    "MetaData": {
      "filename": "example.pdf",
      "filetype": "application/pdf"
    }
  },
  "HTTPRequest": {
    "Method": "POST",
    "URI": "/files/",
    "Header": {
      "Authorization": ["Bearer <jwt-token>"]
    }
  }
}
```

---

## 6. 요약

위의 설정을 통해 다음을 달성했습니다:

1. 프론트엔드가 파일 업로드 시 JWT를 함께 전달합니다;
2. tusd가 요청 헤더를 HTTP hook으로 전달합니다;
3. 백엔드가 django-ninja-jwt를 사용하여 토큰을 검증하고 사용자를 획득합니다;
4. 업로드 권한 부여, 파일 소유권 바인딩 등의 고급 기능을 구현할 수 있습니다.

---

파일 데이터베이스 기록, 권한 검사 또는 사용자 할당량 제한과 같은 기능을 추가하려면 이를 기반으로 로직을 확장할 수 있습니다.

tus는 정말 새로운 시대의 업로드 솔루션입니다 — 재개 가능 업로드는 정말 만족스럽습니다. 아래에 동영상 시연을 첨부합니다.
tus와 django-ninja-jwt를 결합한 재개 가능 업로드 시연입니다.

<video controls width="600">
  <source src="../img/tus断点续传演示.mov" type="video/quicktime">
  Your browser does not support the video tag.
</video>
