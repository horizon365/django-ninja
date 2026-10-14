Django Ninja CRUD Docs
=======================

![Django Ninja CRUD](../img/django-ninja-crud-cover.JPG)


Django Ninja CRUD एक शक्तिशाली, declarative, लेकिन थोड़ा opinionated framework है जो Django Ninja के साथ CRUD (Create, Read, Update, Delete) endpoints के development को सरल बनाता है, और साथ ही Django REST Testing (इस package का छोटा भाई)🐣 का उपयोग करके इन endpoints को test करने के लिए एक declarative, scenario-based approach भी प्रदान करता है। यह आपको common endpoints को class-based views के रूप में परिभाषित करने और उन्हें आसानी से अपनी project की conventions के अनुसार customize करने की अनुमति देता है, और अपने स्वयं के custom views आसानी से बनाने तथा उन्हें प्रदान किए गए CRUD views के साथ declare करने की सुविधा भी देता है, जिससे modularity और extensibility को बढ़ावा मिलता है। यह package इस पर ध्यान केंद्रित करने के लिए प्रोत्साहित करता है जो सबसे महत्वपूर्ण है: वास्तविक दुनिया की समस्याओं को हल करना, न कि अपने project में बार-बार पहिया (wheel) दोबारा आविष्कार करना।


मूल रूप से DRF के ModelViewSet से प्रेरित, Django Ninja CRUD अपनी सीमाओं को दूर करने के लिए विकसित हुआ, true modularity प्राप्त करने के लिए composition-over-inheritance approach अपनाया — जो endpoints बनाने के लिए एक व्यापक declarative interface की ओर एक आधारभूत कदम है।


Inheritance-based viewsets की मुख्य चुनौतियाँ:

*     प्रति model CRUD endpoints की विशिष्टता: Django Ninja CRUD आपको एक ही model के लिए कई endpoints परिभाषित करने की अनुमति देता है, जिससे versioning या alternative representations संभव होती हैं।
*     Customization flexibility: एक monolithic class पर methods को override करने के बजाय, अलग-अलग views को composition और configuration के माध्यम से customize किया जाता है।
*     Inheritance hierarchies के भीतर अंतर्निहित संबंध: composition views को decouple करता है, dependencies को कम करता है और reusability को बेहतर बनाता है।
*     नए endpoints के लिए modularity की कमी: custom endpoints जोड़ने के लिए अब पूरे viewset को subclass करने की आवश्यकता नहीं है, जिससे नई features को incrementally पेश करना आसान हो जाता है।

✨ मुख्य Features
-------

*     पूर्णतः declarative: views और tests को यह declare करके परिभाषित करें कि आप क्या चाहते हैं, न कि यह कैसे करना है।
*     अद्वितीय modularity: viewsets को वांछित CRUD views के साथ customize करें, प्रत्येक view के व्यवहार को customize करते हुए।
*     Extend करने में आसान: अपने स्वयं के custom views बनाएँ और उन्हें प्रदान किए गए CRUD views के साथ reusable components के रूप में उपयोग करें।
*     Scenario-based testing framework: विविध test cases को declarative और संक्षिप्त तरीके से परिभाषित करने के लिए scenario-based testing framework का लाभ उठाएँ।
*     मायने रखने वाली चीज़ों पर ध्यान दें: वास्तविक दुनिया की समस्याओं को हल करने में अधिक समय बिताएँ और common, दोहराव वाले कार्यों पर कम।

> **
> Django Ninja CRUD केवल एक tool नहीं है; यह Django web application development और testing में एक paradigm shift है।**

🫶 समर्थन
----------


सबसे पहले, इस project को support करने के लिए 400+ stargazers का दिल से धन्यवाद। इसकी क्षमता के प्रति आपकी पहचान और भरोसा मुझे इस काम को बनाए रखने और सुधारने, तथा इसे नए संभावित users और contributors के लिए अधिक दृश्य बनाने के लिए प्रेरित करता है।

[![Star History Chart](https://api.star-history.com/svg?repos=hbakri/django-ninja-crud&type=Date)](https://star-history.com/#hbakri/django-ninja-crud&Date)


यदि आपको इस project से लाभ हुआ है या इसके पीछे के समर्पण की सराहना करते हैं, तो आगे का समर्थन देने पर विचार करें। चाहे एक coffee की कीमत हो, प्रोत्साहन का एक शब्द हो, या एक sponsorship, हर इशारा open source की अग्नि में ईंधन जोड़ता है और इसे और अधिक चमकीला बनाता है।✨

[![Sponsor](https://img.shields.io/badge/sponsor-donate-pink?logo=github-sponsors&logoColor=white)](https://github.com/sponsors/hbakri) [![Buy me a coffee](https://img.shields.io/badge/buy_me_a_coffee-donate-pink?logo=buy-me-a-coffee&logoColor=white)](https://www.buymeacoffee.com/hbakri)


आपकी दयालुता और समर्थन का बहुत महत्व है। धन्यवाद!🙏
