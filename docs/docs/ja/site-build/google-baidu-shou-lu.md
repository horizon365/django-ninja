---
comments: true
---
# mkdocs サイトを Google/百度（Baidu）にインデックス登録させる

[前回の記事](add-google-adsense-with-mkdocs.md) では、カスタムテンプレートを使って mkdocs に Google 広告を追加する方法を紹介しました。

その後、Google と百度（Baidu）にサイトを積極的に送信してインデックス登録させることを勧める人が多いことに気づきました。

## Google のインデックス登録

### サイトを追加する

Google Search Console のサイトを開きます：[Google Search Console](https://search.google.com/search-console/welcome?hl=zh-CN)

サイトの所有権の確認を求められます。ここでは HTML タグ方式を使います。

この方法なら、前回の記事で広告を追加したときと同じように、`</head>` の前に 1 行追加して公開するだけです。

### サイトマップ

確認に成功したら、`sitemap.xml` を入力します。数分後に更新すると、ステータスが「取得に成功しました（Fetch successful）」と表示され、これで完了です。

次のコードは、このサイトの sitemap.xml ファイルを解析し、すべてのドキュメントリンクを取得します。

## 百度（Baidu）のインデックス登録

### サイトを追加する

百度のインデックス登録サイトを開きます：[百度搜索资源平台（Baidu Search Resource Platform）](https://ziyuan.baidu.com/dailysubmit/index)

上記の Google の確認と同様に、HTML タグによる確認を使います。

### サイトマップ
ICP 备案番号を記入しなかったためだと思われますが、サイトマップのセクションがグレーアウトしていました。そこで手動送信を選びました。1 日あたり最大 20 件までという点に注意してください。

サイトのすべてのリンクは、次のスクリプトで取得できます。

```python
import urllib.request
import xml.etree.ElementTree as ET


def parse_and_save_loc(url, output_file):
    # Fetch the XML data from the online address
    response = urllib.request.urlopen(url)
    data = response.read()

    # Parse the XML
    root = ET.fromstring(data)

    # Extract all loc attributes and save them to a TXT file
    with open(output_file, 'w') as f:
        for element in root.iter():
            if 'loc' in element.tag:
                print(element.text)
                f.write(element.text + '\n')


# Specify the online XML file address and the output TXT file path
url = 'https://django-ninja.cn/sitemap.xml'
output_file = 'urls.txt'

parse_and_save_loc(url, output_file)
```

> 参考記事：
    1. [ゼロから作る個人ブログサイト シリーズ](https://www.techxiaofei.com/post/hugo/hugo_search/#%E8%B0%B7%E6%AD%8C%E6%94%B6%E5%BD%95)
  
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
