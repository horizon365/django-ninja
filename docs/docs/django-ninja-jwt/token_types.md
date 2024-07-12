
Ninja JWT 提供了两种不同的令牌类型，可用于证明身份验证。
在令牌的有效负载中，其类型可以通过其令牌类型声明的值来识别，默认情况下该声明为 `token_type`。
然而，这可能具有 `access`（访问）、`sliding`（滑动）或 `refresh`（刷新）的值，
但目前刷新令牌不被视为有效的身份验证令牌。用于存储类型的声明名称可以通过更改 `TOKEN_TYPE_CLAIM` 设置来定制。

默认情况下， Ninja JWT 期望一个 `access` 令牌来证明身份验证。
允许的身份验证令牌类型由 `AUTH_TOKEN_CLASSES` 设置的值决定。 
该设置包含一个指向令牌类的点路径列表。它默认包含 `'ninja_jwt.tokens.AccessToken'` 点路径，
但也可能包括 `'ninja_jwt.tokens.SlidingToken'` 点路径。
这些点路径中的任意一个或两个都可以出现在身份验证令牌类列表中。
如果它们都存在，那么这两种令牌类型都可以用于证明身份验证。

滑动令牌
==============

滑动令牌为令牌用户提供了更方便的体验，但也存在安全性较低以及在使用黑名单应用程序的情况下性能较低的权衡。
滑动令牌是一种同时包含过期声明和刷新过期声明的令牌。只要滑动令牌过期声明中的时间戳尚未过去，
它就可以用于证明身份验证。此外，只要其刷新过期声明中的时间戳尚未过去，
它也可以提交给刷新视图以获取具有更新过期声明的自身副本。

如果你想使用滑动令牌，请将 `AUTH_TOKEN_CLASSES` 设置更改为 `('ninja_jwt.tokens.SlidingToken',)`。
(或者，如果您希望允许两种令牌类型都用于身份验证，`AUTH_TOKEN_CLASSES` 设置可能包括指向 `ninja_jwt.tokens` 
模块中 `AccessToken` 和 `SlidingToken` 令牌类的点路径)

此外，将 `NinjaJWTSlidingController` 注册到 `api`:
```python
from ninja_jwt.controller import NinjaJWTSlidingController
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTSlidingController)

```

请注意，如果你正在使用黑名单应用程序， Ninja JWT 将针对每个经过身份验证的请求对所有滑动令牌与黑名单进行验证。
这将降低经过身份验证的 API 视图的性能。

<img style="object-fit: cover; object-position: 50% 50%;" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
