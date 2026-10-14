`ninja_schema` और `ninja` के अंदर का schema बहुत अलग महसूस होते हैं — ninja का काम करता है, लेकिन `ninja_schema` में वाला एक error raise करता है
==========================================================

A: क्या `ninja_schema` एक अलग package है?
B: हाँ, इसे pip से install करने की आवश्यकता है। मैंने सोर्स कोड देखा, और लगता है कि इसने pydantic से कुछ चीज़ें खींची हैं। लेकिन मैं pydantic को नहीं समझता, इसलिए मुझे ठीक से नहीं पता कि नई जोड़ी गई चीज़ें कौन सी functionality implement करती हैं।

A: मुझे लगता है कि ninja का schema पर्याप्त से अधिक है।
B: Foreign key output को flatten करने के लिए, documentation इसका उपयोग इस प्रकार करती है: `owner_first_name: str = Field(None, alias="owner.first_name")`
B: `ninja_schema` वाले का उपयोग करने पर बार-बार error आता है, जिसमें कहा जाता है कि input एक `str` होना चाहिए, लेकिन जो दिया गया है वह एक object है।
B: मैंने कभी नहीं सोचा था कि `ninja_schema` का यह `Schema` ही कारण था।
