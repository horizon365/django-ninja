---
comments: true
---
# **チュートリアル / リファレンス**

このチュートリアルでは、**Django Ninja Extra** とそのほとんどの機能の使い方を説明します。
特に、**Django Ninja** の使い方をすでに知っていることを前提としています。


!!! info
    ここで説明する内容の多くは Django-Ninja に由来しています。そのため、先に Django-Ninja フレームワークについて学んでおくと、内容が理解しやすくなります。

## **インストール**

```
pip install django-ninja-extra
```

インストール後、`ninja_extra` を `INSTALLED_APPS` に追加します

```Python 
INSTALLED_APPS = [
    ...,
    'ninja_extra',
]
```


## **Django プロジェクトの作成**

（すでに既存の Django プロジェクトがある場合は、次のステップに進んでください）。

新しい Django プロジェクトを開始します（または既存のプロジェクトを使用します）。

```
django-admin startproject myproject
```


## **最初のステップ**

API 用のモジュールを作成しましょう。**urls.py** と同じディレクトリに **api.py** ファイルを作成します：


`api.py`


```Python
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()

# function definition using Django-Ninja default router
@api.get("/hello")
def hello(request):
    return "Hello world"

```

次に **urls.py** を開いて、以下を追加します：


```Python hl_lines="3 7"
from django.contrib import admin
from django.urls import path
from .api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
```

## **操作（オペレーション）メソッドの定義**
「オペレーション」とは、HTTP の「メソッド」のいずれかです：

 - GET
 - POST
 - PUT
 - DELETE
 - PATCH
 - ... など。

これらは、Django-Ninja が API や Django-Ninja ルータ上に定義しているオペレーションです。

同じオペレーションが、`route` クラスを通じて APIController にも公開されています。

`route` クラスは、APIController のインスタンスメソッドをルート関数（エンドポイント）に変換する追加のデコレータです。

一方で、ここでの `route` は `ControllerRouter` クラスの略称でもあります。これは APIController を Django-Ninja ルータに適合させるアダプタクラスで、任意の APIController クラスに定義されたすべてのルートをグローバルに制御することもできます。

```Python
from ninja_extra import (
    api_controller, 
    http_get, http_post, http_put, http_delete, http_patch, http_generic
)
from ninja.constants import NOT_SET

@api_controller('', tags=['My Operations'], auth=NOT_SET, permissions=[])
class MyAPIController:
    @http_get("/path")
    def get_operation(self):
        ...
    
    @http_post("/path")
    def post_operation(self):
        ...
    
    @http_put("/path")
    def put_operation(self):
        ...
    
    @http_delete("/path")
    def delete_operation(self):
        ...
    
    @http_patch("/path")
    def patch_operation(self):
        ...
    
    # If you need to handle multiple methods with a single function, you can use the `generic` method as shown above
    @http_generic(["POST", "PATCH"]) 
    def mixed(request):
        ...

api.register_controllers(MyAPIController)
```
コントローラの設定を完了するには、登録する前に APIController を `ControllerRouter` でデコレートする必要があります。


<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
