---
comments: true
---
好的，下面是一篇适合写在 Markdown 博客中的中文技术文章，介绍如何使用 `django-ninja-jwt` 与 `tusd` 的 HTTP Hooks 对接，实现用户身份验证。

---

# 使用 django-ninja-jwt 对接 tusd 的 HTTP Hooks 实现用户认证

在构建支持断点续传的大文件上传服务时，[`tusd`](https://github.com/tus/tusd) 是一个非常流行的服务端实现。而在 Django 项目中，我们通常会使用 [django-ninja](https://django-ninja.dev) 框架配合 [django-ninja-jwt](https://pypi.org/project/django-ninja-jwt/) 进行 API 开发和身份认证。

本篇文章将介绍如何通过 **tusd 的 HTTP Hooks**，结合 `django-ninja-jwt` 实现用户身份识别和上传权限控制。

---

## 一、tusd 的 HTTP Hooks 简介

`tusd` 支持在上传生命周期的各个阶段触发 Hook（比如 `pre-create`, `post-finish`），你可以配置 `--hooks-http` 参数，让 `tusd` 在触发 Hook 时发送一个 HTTP 请求。

示例配置命令：

```bash
tusd \
  -hooks-http http://localhost:8000/tusd-hook/ \
  -cors-allow-origin "http://localhost:8080" \
  -cors-allow-credentials \
  -upload-dir ./uploads
```

当某个上传操作发生时，tusd 会向指定地址 POST 一段 JSON，其中包含请求头（如 `Authorization` 或 `Cookie`）和上传的元数据。

---

## 二、tus-js-client 配置 JWT 请求头

在前端（比如 Vue/Quasar 应用）中使用 `tus-js-client` 时，需要将 JWT Token 附加在请求头中发送：

```js
import tus from 'tus-js-client'

const upload = new tus.Upload(file, {
  endpoint: 'http://localhost:1080/files/',
  metadata: {
    filename: file.name,
    filetype: file.type
  },
  headers: {
    Authorization: 'Bearer ' + localStorage.getItem('access_token') // JWT 令牌
  },
  withCredentials: false, // 不走 cookie，使用 Authorization 头
  onError: (error) => console.error(error),
  onSuccess: () => console.log('上传成功')
})

upload.start()
```

---

## 三、后端：Django 接收 tusd Hook 并校验 JWT

在 Django 项目中创建一个 Hook 接收接口：

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

            # 使用 django-ninja-jwt 的 JWTAuth 解析 token
            user = JWTAuth().authenticate(request, token)

            if user is None:
                return JsonResponse({"error": "Invalid token"}, status=401)

            # user 为通过认证的 Django User 实例
            print("上传用户：", user.username)

            # 可根据用户信息进行鉴权或写入数据库等操作
            return JsonResponse({"status": "ok"})

        return JsonResponse({"error": "No token"}, status=401)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
```

---

## 四、注册路由

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

## 五、tusd Hook 请求示例（POST）

tusd 会向后端发送类似这样的 JSON：

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

## 六、总结

通过上述配置，我们实现了：

1. 前端上传文件时携带 JWT；
2. tusd 将请求头传入 HTTP hook；
3. 后端用 django-ninja-jwt 验证 token 并获取用户；
4. 可实现上传鉴权、文件归属绑定等高级功能。

---

如果你还想加入文件数据库记录、权限校验、用户配额限制等功能，可以在这个基础上扩展逻辑。

tus真是新时代的上传方案，断点续传太爽了。附上视频演示。
搭配django-ninja-jwt的tus断点续传演示

<video controls width="600">
  <source src="../img/tus断点续传演示.mov" type="video/quicktime">
  您的浏览器不支持 video 标签。
</video>
