---
created: 2024-07-25T13:23:12 (UTC +08:00)
tags: []
source: https://medium.com/@mrclemrkz/django-ninja-python-framework-for-rest-api-83808d1037d0
author: Clement Fernando

---


Django-Ninja: REST APIs के लिए एक Python Framework
===========================================================



> मैं हाल ही में एक REST API में बहुत सरल CRUD service बनाना चाहता था। ढूँढने के बाद, मुझे एक सरल framework मिला जो दो लोकप्रिय frameworks की सर्वोत्तम features को combine करता है। वह है Django-ninja...

* * *


TL;DR
-----


मैं हाल ही में एक REST API में बहुत सरल CRUD service बनाना चाहता था। ढूँढने के बाद, मुझे एक सरल framework मिला जो दो लोकप्रिय frameworks की सर्वोत्तम features को combine करता है। वह है Django-ninja; मैं इसे Django और FastAPI का संयोजन मानता हूँ।

---
मुझे यह समझाने दें कि मैं इसे एक लाभदायक approach क्यों मानता हूँ।


अपनी पृष्ठभूमि पर प्रकाश डालने के लिए, मैं एक Python Django developer हूँ और Flask में कुछ projects कर चुका हूँ।


FastAPI की लोकप्रियता के साथ, मैं पहले इसे आज़माना चाहता था। इसलिए मैंने documentation के अनुसार इसके examples चलाए, और अनुभव यह था कि, वाह, यह बढ़िया है। फिर Pydantic के उपयोग ने मुझे उत्साहित कर दिया। सबसे महत्वपूर्ण बात, यह async पर built है। Swagger UI पर OpenAPI की सहज और आसान generation ने इसे और भी मीठा बना दिया।


यह मेरे लिए एक आँख खोलने वाला अनुभव था। इसलिए, मैंने गहराई से खोजना शुरू किया।


वहीं मुझे पता चला कि चूँकि FastAPI Django की तरह "batteries-included" नहीं है, इसमें अभी भी एक ORM (SQLAlchemy या SQLModel) configure करने की आवश्यकता होती है, database migration tools जैसे Alembic के लिए तो एक और third-party package की आवश्यकता का तो ज़िक्र ही छोड़ दें।


तो, मैंने सोचा, क्या बाहर कोई बेहतर solution है, जो कम configuration के साथ अधिक स्थिर हो। हो सकता है कोई ऐसी चीज़ हो जिस पर अभी तक ध्यान नहीं गया हो। फिर मैंने खोजना शुरू किया।


मैंने सभी विकल्पों में से कुछ को सूचीबद्ध किया (सितंबर 2023 तक GitHub stars):


Flask: 64K stars — पहली release: 1 अप्रैल, 2010


FastAPI: 61.8K stars — पहली release: 5 दिसंबर, 2018


Django Rest Framework: 26.2K stars — पहली release: 21 जुलाई, 2005


Sanic: 17.3K stars — पहली release: 23 अक्टूबर, 2016


Django Ninja: 4.8K stars — पहली release: 20 दिसंबर, 2020


तो, स्पष्ट रूप से मैं Django Ninja में रुचि लेने लगा, और यहाँ वे कारण हैं जिनसे मुझे लगता है कि यह अच्छा है।

**लोकप्रियता**
--------------


Django-Ninja, Django पर built है, जो सबसे लोकप्रिय और स्पष्ट web framework है। Django-Ninja को पहली बार 2020 के अंत में release किया गया था, और लगभग 3 साल में ही इसने महत्वपूर्ण लोकप्रियता हासिल की है।

**सामान्य Project Structure**
-----------


Flask और FastAPI के विपरीत, Django project बनाते समय एक structure impose करता है। हालाँकि, project को maintain करने के आपके तरीके के मामले में यह अधिक लचीला है। यह एक ऐसी चीज़ है जो मुझे Django में पसंद है, क्योंकि इससे किसी अन्य Django developer के लिए project को समझना काफी आसान हो जाता है।


हाँ, Django Rest Framework (DRF) भी यह कर सकता है। लेकिन मैंने "rapid development" कहा था, है ना? Simple और organized code को कौन नहीं पसंद करता? Django-Ninja का उपयोग करने की सुंदरता यही है।

**शक्तिशाली ORM**
------------


फिर, शक्तिशाली core framework (Django) से जुड़ा होना Django-Ninja में प्रतिष्ठा लाता है।


कम सुरक्षित तरीके से स्वयं SQL queries लिखने के बजाय, हम ORMs का उपयोग करना पसंद करते हैं। यह simple और सुरक्षित database calls लिखने में मदद करता है।


हालाँकि, बेशक, Django ORM और SQLAlchemy ORM की concepts अलग-अलग हैं। Django ORM Active Record pattern का उपयोग करता है, जबकि SQLAlchemy Data Mapper pattern का उपयोग करता है, जिसे बाद में एक अन्य blog में विस्तार से समझाया जाएगा।

**  
उपयोग में आसान API Documentation
-----------------


हाँ, DRF (Django Rest Framework) का अपना API documentation है। लेकिन मेरी राय में, OpenAPI Swagger UI कहीं बेहतर है। इसलिए जब मुझे DRF के साथ Swagger UI चाहिए था, तो मैंने drf-yasg नामक एक swagger generator package का उपयोग किया, जिसने काफी अच्छा काम किया।


लेकिन FastAPI की तरह, Django-Ninja में, आप url function के अलावा कोई अतिरिक्त कोड लिखे बिना एक interactive OpenAPI Swagger UI प्राप्त कर सकते हैं।

**प्रदर्शन (Performance)**
---------------


FastAPI की तरह, इसमें Pydantic के माध्यम से built-in type enforcement support और asynchronous execution है।


Django-ninja की documentation ने Flask, DRF और Django-ninja के बीच benchmark data की तुलना करके इस बात की डींग भी नहीं भूली।

**तेज़ delivery**
-------------------


फिर, बिल्कुल FastAPI की तरह, यह बहुत कम code base के साथ एक REST API service शुरू कर सकता है। साथ ही, यह आपको आपके द्वारा उचित समझी गई किसी भी दार्शनिक approach के अनुसार आसानी से develop करने में मदद करता है। विशेषाधिकार की सुंदरता यही है।


एक न्यूनतम और संक्षिप्त code base उच्च readability की ओर ले जाता है। यह बदले में तेज़ implementation के लिए intuition को बढ़ावा देता है।


इस पर आपकी क्या comments, thoughts और राय हैं? नीचे comments में मुझे बताएं।
