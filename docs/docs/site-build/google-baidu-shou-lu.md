# 谷歌/百度收录 mkdocs 网站

在[上篇文章中](add-google-adsense-with-mkdocs.md) 我们介绍了如何通过自定义模板在 mkdocs 中增加 google ads。

后面发现好多人推荐主动去做谷歌和百度的收录。

## 谷歌收录

### 添加网站

打开谷歌收录网站： [Google Search Console](https://search.google.com/search-console/welcome?hl=zh-CN)

会提示你需要验证对网站的所有权，这里我们通过 HTML 标记的方式。

这样，只需要和上篇文章添加 ads 一样的步骤，在 `</head>` 前添加一行然后发布就行。

### 站点地图
验证成功后，输入 `sitemap.xml` ，然后隔几分钟，刷新发现状态为 抓取成功 就行了。

以下代码通过解析本站的 sitemap.xml 文件，获取所有的 doc 链接

## 百度收录

### 添加网站

跟上面的谷歌验证类似，使用 HTML 标签验证。

### 站点地图
可能是因为我没填写备案号，sitemap那里我是灰色的。所以我选择了手动提交。注意，每天最多 20 条。

网络的所有链接通过以下脚本可以获取到。

```python
import urllib.request
import xml.etree.ElementTree as ET


def parse_and_save_loc(url, output_file):
    # 从在线地址获取 XML 数据
    response = urllib.request.urlopen(url)
    data = response.read()

    # 解析 XML
    root = ET.fromstring(data)

    # 提取所有 loc 属性并保存到 TXT 文件
    with open(output_file, 'w') as f:
        for element in root.iter():
            if 'loc' in element.tag:
                print(element.text)
                f.write(element.text + '\n')


# 指定在线 XML 文件的地址和输出 TXT 文件的路径
url = 'https://django-ninja.cn/sitemap.xml'
output_file = 'urls.txt'

parse_and_save_loc(url, output_file)
```

> 参考文章:
    1. [从零开始搭建个人博客网站系列](https://www.techxiaofei.com/post/hugo/hugo_search/#%E8%B0%B7%E6%AD%8C%E6%94%B6%E5%BD%95)
  