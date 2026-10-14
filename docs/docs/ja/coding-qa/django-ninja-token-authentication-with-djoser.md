# Django Ninja と Djoser によるトークン認証


Source URL: https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser


この質問は調査の努力が見られ、有用で明確です

2

この質問を保存します。

[](https://stackoverflow.com/posts/70716976/timeline)


この投稿のアクティビティを表示します。


Django Ninja フレームワークを使って CRUD を実装しましたが、アプリケーションで認証を行いたいと思っています。Djoser をインストールして設定済みなので、トークンを生成できるようになりましたが、そのトークンを自分の CRUD 内で検証する方法がわかりません

    class AuthBearer(HttpBearer):
        def authenticate(self, request, token):
            if token == "supersecret":
                return token
    
    @api.get("/bearer", auth=AuthBearer())
    def bearer(request):
        return {"token": request.auth}



"AuthBearer" 関数内でトークンをチェックできるはずなのですが、その方法がわかりません

私のリポジトリ（[リンク](https://github.com/arsalanses/ham-radio-logger/blob/master/logs/api/v1.py)）

*   [django](https://stackoverflow.com/questions/tagged/django "show questions tagged 'django'")
*   [django-rest-framework](https://stackoverflow.com/questions/tagged/django-rest-framework "show questions tagged 'django-rest-framework'")
*   [djoser](https://stackoverflow.com/questions/tagged/djoser "show questions tagged 'djoser'")
*   [django-ninja](https://stackoverflow.com/questions/tagged/django-ninja "show questions tagged 'django-ninja'")

[共有](https://stackoverflow.com/q/70716976 "Short permalink to this question")


この質問へのリンクを共有する

リンクをコピー[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/ "The current license for this post: CC BY-SA 4.0")

[この質問を改善する](https://stackoverflow.com/posts/70716976/edit)

フォロー


通知を受け取るためにこの質問をフォローする

[2022 年 12 月 8 日 17:18 に編集](https://stackoverflow.com/posts/70716976/revisions "show all edits to this post")

[![Image 1: metersk's user avatar](https://www.gravatar.com/avatar/f1a23a45808b0429be1543ca726d522f?s=64&d=identicon&r=PG)](https://stackoverflow.com/users/1887261/metersk)

[metersk](https://stackoverflow.com/users/1887261/metersk)

12.3k2222 金バッジ6868 銀バッジ103103 銅バッジ


質問日時：2022 年 1 月 14 日 21:59

[![Image 2: Arsalan's user avatar](https://i.sstatic.net/R9DYa.jpg?s=64)](https://stackoverflow.com/users/3711191/arsalan)

[Arsalan](https://stackoverflow.com/users/3711191/arsalan)Arsalan

7722 銀バッジ99 銅バッジ

[コメントを追加](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Use comments to ask for more information or suggest improvements. Avoid answering questions in comments.") |[](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Expand to show all comments on this post")

1 件の回答 1
----------


並び順: デフォルトにリセット


スコアが高い順（デフォルト） トレンド（最近の投票がより多くカウントされる） 更新日順（新しいものが先） 作成日順（古いものが先）


この回答は役に立ちます

6

回答を保存します。

[](https://stackoverflow.com/posts/70720995/timeline)


この投稿のアクティビティを表示します。


基本的には、Ninja の `HttpBearer` クラスを継承し、`authenticate` メソッドを実装する必要があります。このメソッドは引数として request と token を受け取ります。このメソッドは、ユーザーが認証されていない場合は `None` を返し、認証されている場合は `request.auth` に格納される文字列を返します。通常、この文字列はユーザー名になるので、すべてのエンドポイントでそれを使うことができます。たとえば次のような感じです（私は PyJWT を使ってトークンをデコードしています）:

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



[共有](https://stackoverflow.com/a/70720995 "Short permalink to this answer")


この回答へのリンクを共有する

リンクをコピー[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/ "The current license for this post: CC BY-SA 4.0")

[この回答を改善する](https://stackoverflow.com/posts/70720995/edit)

フォロー


通知を受け取るためにこの回答をフォローする


回答日時：2022 年 1 月 15 日 11:30 AM

[![Image 3: abolfazlmalekahmadi's user avatar](https://i.sstatic.net/CeWmU.png?s=64)](https://stackoverflow.com/users/10356618/abolfazlmalekahmadi)

[abolfazlmalekahmadi](https://stackoverflow.com/users/10356618/abolfazlmalekahmadi)abolfazlmalekahmadi

26822 銀バッジ1717 銅バッジ

1

* このコード例をありがとう！エンコードされたトークンはどのように生成するのですか？これらのトークンをストレージに保存するのですか？

  –[netcyrax](https://stackoverflow.com/users/2456568/netcyrax "1,089 reputation")

  [  
  コメント日時：2023 年 7 月 18 日 9:29](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser#comment135243481_70720995)

[コメントを追加](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Use comments to ask for more information or suggest improvements. Avoid comments like “+1” or “thanks”.") |[](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Expand to show all comments on this post")

@media (prefers-color-scheme: dark) { body { color: #fff !important; background-color: #272727 !important; } } body { overflow-y: hidden; }
