---
comments: true
---
नीचे एक तकनीकी लेख दिया गया है जो Markdown blog के लिए उपयुक्त है, जिसमें यह बताया गया है कि `django-ninja-jwt` का उपयोग करके `tusd` के HTTP Hooks के साथ user authentication कैसे integrate करें।

---

# django-ninja-jwt का उपयोग करके tusd के HTTP Hooks के साथ User Authentication को Integrate करना

जब resumable uploads को support करने वाली large-file upload services बनाई जाती हैं, तो [`tusd`](https://github.com/tus/tusd) एक बहुत लोकप्रिय server-side implementation है। Django projects में, हम आमतौर पर API development और authentication के लिए [django-ninja](https://django-ninja.dev) framework के साथ [django-ninja-jwt](https://pypi.org/project/django-ninja-jwt/) का उपयोग करते हैं।

यह लेख यह बताएगा कि **tusd के HTTP Hooks** को `django-ninja-jwt` के साथ कैसे combine किया जाए ताकि user identification और upload permission control प्राप्त किया जा सके।

---

## 1. tusd के HTTP Hooks का परिचय

`tusd` upload lifecycle के विभिन्न चरणों (जैसे `pre-create`, `post-finish`) में Hooks को trigger होने की सुविधा देता है। आप `--hooks-http` parameter configure कर सकते हैं ताकि Hook trigger होने पर `tusd` एक HTTP request भेजे।

Configuration command का उदाहरण:

```bash
tusd \
  -hooks-http http://localhost:8000/tusd-hook/ \
  -cors-allow-origin "http://localhost:8080" \
  -cors-allow-credentials \
  -upload-dir ./uploads
```

जब कोई upload operation होता है, तो tusd निर्दिष्ट address पर एक JSON payload POST करेगा, जिसमें request headers (जैसे `Authorization` या `Cookie`) और upload metadata शामिल होते हैं।

---

## 2. tus-js-client के साथ JWT Request Header को Configure करना

Frontend पर `tus-js-client` का उपयोग करते समय (उदाहरण के लिए, Vue/Quasar application में), आपको request header में JWT Token attach करने की आवश्यकता होती है:

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

## 3. Backend: Django tusd Hook को प्राप्त करता है और JWT को सत्यापित करता है

अपने Django project में एक Hook receiving endpoint बनाएं:

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

## 4. Route को Register करना

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

## 5. tusd Hook Request (POST) का उदाहरण

tusd backend को निम्नलिखित जैसा JSON भेजेगा:

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

## 6. सारांश

ऊपर दी गई configuration के माध्यम से, हमने हासिल किया:

1. Frontend file upload करते समय JWT साथ रखता है;
2. tusd request headers को HTTP hook तक पहुँचाता है;
3. Backend django-ninja-jwt का उपयोग करके token सत्यापित करता है और user प्राप्त करता है;
4. Upload authorization और file ownership binding जैसी advanced features implement की जा सकती हैं।

---

यदि आप file database records, permission checks, या user quota limits जैसी features जोड़ना चाहते हैं, तो आप इस आधार पर logic को विस्तारित (extend) कर सकते हैं।

tus वास्तव में नए युग का upload solution है — resumable uploads कितने संतोषजनक हैं। नीचे एक video प्रदर्शन संलग्न है।
tus के django-ninja-jwt के साथ resumable uploads का एक प्रदर्शन।

<video controls width="600">
  <source src="../img/tus断点续传演示.mov" type="video/quicktime">
  Your browser does not support the video tag.
</video>
