---
comments: true
---
# Verifying Google Domain Ownership on Huawei Cloud

If you want to enable Google Analytics, you first need to verify domain ownership.

There are two methods. One is via the URL prefix: for example, if you enter `https://pingti.ren/`, then all URLs under it can be monitored, but there is a drawback. Subdomains cannot be monitored — for example, `https://docs.pingti.ren/` cannot be monitored.
So Google has the concept of domain verification. As long as it is related to `pingti.ren`, it can all be covered.

As for which is better, it depends on individual needs. If you have many subdomains, then of course it's better to verify them all at once via a domain.

Here I'll talk about how to fill in the TXT record on Huawei Cloud to pass Google's domain verification. There is basically no information available online; I figured it out on my own.

The key point is to select the TXT type, leave Name blank, and fill in the Value with the code Google gives you, such as "google-site-verification=xxxx-xxxxx". And it must be wrapped in quotes. The complete configuration is shown in the figure:

!(google-site-verification)[/img/huaweicloud-google-site-verification.png]

This is the domain verification method recommended by Google. You can also do it via CNAME, but it requires two records.

Once verification passes, adding a sitemap in the Google console becomes very flexible, without the URL prefix restriction.

!(google-console-domain-add-sitemap)[/img/google-console-domain-add-sitemap]

As you can see, it's very convenient to add various subdomains.
