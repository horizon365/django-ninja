---
comments: true
---
# 华为云（Huawei Cloud）で Google のドメイン所有権を確認する

Google Analytics を有効にしたい場合、まずドメインの所有権を確認する必要があります。

方法は 2 つあります。1 つは URL プレフィックスによるもので、たとえば `https://pingti.ren/` を入力すると、その配下のすべての URL をモニタリングできますが、欠点があります。サブドメインはモニタリングできません — たとえば `https://docs.pingti.ren/` はモニタリングできません。
そのため Google にはドメイン検証という概念があります。`pingti.ren` に関連するものであれば、すべてカバーできます。

どちらが良いかは、個々のニーズによります。サブドメインが多いなら、もちろんドメイン単位で一度に確認する方が良いでしょう。

ここでは、华为云（Huawei Cloud）で TXT レコードを入力して Google のドメイン検証を通過させる方法を説明します。ネット上にはほとんど情報がなく、自分で試行錯誤して見つけました。

ポイントは、タイプとして TXT を選び、Name は空のままにし、Value に Google から渡されるコード（たとえば "google-site-verification=xxxx-xxxxx"）を入力することです。そして、必ず引用符で囲む必要があります。完全な設定は図のとおりです：

!(google-site-verification)[/img/huaweicloud-google-site-verification.png]

これは Google が推奨するドメイン検証の方法です。CNAME でも可能ですが、2 つのレコードが必要になります。

検証に通れば、Google コンソールでのサイトマップの追加は非常に柔軟になり、URL プレフィックスの制限を受けません。

!(google-console-domain-add-sitemap)[/img/google-console-domain-add-sitemap]

ご覧のとおり、さまざまなサブドメインを追加するのがとても便利です。
