---
comments: true
---
# 在华为云上验证谷歌网域所有权

如果想要启用Google Analytic，那么首先需要验证域名所有权。

有两种方式，一种是通过网址前缀：例如你填写了 https://pingti.ren/ 那么它下面所有的网址都能被监控到，但是有一个缺点。 子域名不能监测，例如 https://docs.pingti.ren/ 这个不能监测到。
所以对应的谷歌上有网域验证一说。只要你和 pingti.ren 相关的，都能控制住。

至于哪种好，看各人需求。如果你有很多子域名，那么当然是通过网域一次性完整验证比较好。

这里讲讲如何在华为云上填写 TXT 记录，来通过谷歌的网域验证，网上基本查不到资料，都是自己摸索。

关键的点在于，选择 TXT 类型，然后 Name不用填写， Value 填写谷歌给的代码，例如"google-site-verification=xxxx-xxxxx"。并且要用引号包裹， 完整的配置如图：

!(google-site-verification)[/img/huaweicloud-google-site-verification.png]

这种是谷歌推荐的网域验证方法，通过CNAME也可以 ，但是需要两条。

那验证通过后，在 google console 中添加站点地图时候，也就很灵活，没有了网址前缀的限制。

!(google-console-domain-add-sitemap)[/img/google-console-domain-add-sitemap]

可以看到很方便添加各种子域名。
