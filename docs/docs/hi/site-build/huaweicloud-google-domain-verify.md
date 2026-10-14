---
comments: true
---
# Huawei Cloud पर Google Domain Ownership verify करना

अगर आप Google Analytics enable करना चाहते हैं, तो पहले आपको domain ownership verify करनी होगी।

दो methods हैं। एक URL prefix के ज़रिए है: उदाहरण के लिए, अगर आप `https://pingti.ren/` enter करते हैं, तो उसके अंतर्गत आने वाले सभी URLs monitor किए जा सकते हैं, लेकिन एक कमी है। Subdomains monitor नहीं किए जा सकते — उदाहरण के लिए, `https://docs.pingti.ren/` monitor नहीं हो सकता।
इसलिए Google में domain verification की concept है। जब तक वह `pingti.ren` से संबंधित है, सब कुछ covered हो जाएगा।

जो बेहतर है, वह व्यक्तिगत ज़रूरतों पर निर्भर करता है। अगर आपके पास कई subdomains हैं, तो बेशक domain के ज़रिए एक साथ सभी को verify करना बेहतर है।

यहाँ मैं बताऊँगा कि Huawei Cloud पर Google की domain verification pass करने के लिए TXT record कैसे भरें। Internet पर इसकी जानकारी लगभग नहीं के बराबर है; मैंने खुद ही इसे ढूँढ निकाला।

मुख्य बात यह है कि TXT type चुनें, Name खाली छोड़ दें, और Value में Google द्वारा दिया गया code भरें, जैसे "google-site-verification=xxxx-xxxxx"। और इसे quotes में wrap करना ज़रूरी है। पूरी configuration figure में दिखाई गई है:

!(google-site-verification)[/img/huaweicloud-google-site-verification.png]

यह वह domain verification method है जिसकी सलाह Google देता है। आप यह CNAME के ज़रिए भी कर सकते हैं, लेकिन इसमें दो records चाहिए।

Verification pass होने के बाद, Google console में sitemap जोड़ना बहुत flexible हो जाता है, URL prefix की सीमा के बिना।

!(google-console-domain-add-sitemap)[/img/google-console-domain-add-sitemap]

जैसा कि आप देख सकते हैं, विभिन्न subdomains जोड़ना बहुत आसान है।
