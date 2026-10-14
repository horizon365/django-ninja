**API Controller Route Decorators**
===================

  
`route` class एक function decorator है जिसका उपयोग Controller class के functions को एक specific HTTP method के साथ endpoints के रूप में annotate करने के लिए किया जाता है।

उदाहरण के लिए:

    from ninja_extra import route, api_controller
    
    @api_controller
    class MyController:
        @route.get('/test')
        def test(self):
            return {'message': 'test'}
    

  
`route` predefined methods प्रदान करता है जो विभिन्न operations बनाने को सरल बनाते हैं, और उनके नाम संबंधित HTTP methods के अनुरूप होते हैं:

*   GET: `route.get`
*   POST: `route.post`
*   PUT: `route.put`
*   DELETE: `route.delete`
*   PATCH: `route.patch`
*     
    Generic - operations संयोजनों के लिए उपयोग किया जाता है, जैसे `route.generic(methods=['POST', 'PATCH'])`

**  
Initialization Parameters**
------------

  
नीचे NinjaExtra में `route` class के parameters का एक अवलोकन विवरण दिया गया है:

*     
    `path`: आवश्यक unique endpoint path string।
    
*     
    `methods`: endpoint के लिए आवश्यक HTTP methods का संग्रह, जैसे `['POST', 'PUT']`।
    
*     
    `auth`: endpoint के लिए authentication method परिभाषित करता है। डिफ़ॉल्ट: `NOT_SET`
    
*     
    `response`: response format को `dict[status_code, schema]` या `Schema` के रूप में परिभाषित करता है। Return किए गए response को validate करने के लिए उपयोग किया जाता है। डिफ़ॉल्ट: `NOT_SET`
    
*     
    `operation_id`: एक वैकल्पिक unique identifier जिसका उपयोग path views में operations को अलग करने के लिए किया जाता है। डिफ़ॉल्ट: `NOT_SET`
    
*     
    `summary`: एक वैकल्पिक सारांश जिसका उपयोग endpoint का वर्णन करने के लिए किया जाता है। डिफ़ॉल्ट: `None`
    
*     
    `description`: एक वैकल्पिक विवरण जो endpoint के बारे में अतिरिक्त जानकारी प्रदान करता है। डिफ़ॉल्ट: `None`
    
*     
    `tags`: strings की एक list जिसका उपयोग documentation के उद्देश्यों के लिए endpoints को group करने के लिए किया जाता है। डिफ़ॉल्ट: `None`
    
*     
    `deprecated`: एक वैकल्पिक boolean parameter जो दर्शाता है कि endpoint deprecated है या नहीं। डिफ़ॉल्ट: `None`
    
*     
    `by_alias`: एक वैकल्पिक parameter जिसका उपयोग `response` schema object को filter करने के लिए किया जाता है। डिफ़ॉल्ट: `False`
    
*     
    `exclude_unset`: एक वैकल्पिक parameter जिसका उपयोग `response` schema object को filter करने के लिए किया जाता है। डिफ़ॉल्ट: `False`
    
*     
    `exclude_defaults`: एक वैकल्पिक parameter जिसका उपयोग `response` schema object को filter करने के लिए किया जाता है। डिफ़ॉल्ट: `False`
    
*     
    `exclude_none`: एक वैकल्पिक parameter जिसका उपयोग `response` schema object को filter करने के लिए किया जाता है। डिफ़ॉल्ट: `False`
    
*     
    `include_in_schema`: दर्शाता है कि endpoint Swagger documentation में दिखाई देना चाहिए या नहीं। डिफ़ॉल्ट: `True`
    
*     
    `url_name`: endpoint के लिए एक नाम प्रदान करता है जिसे Django में `reverse` function का उपयोग करके resolve किया जा सकता है। डिफ़ॉल्ट: `None`
    
*     
    `permissions`: endpoint के लिए route permission classes का संग्रह परिभाषित करता है। डिफ़ॉल्ट: `None`
    

  
ये parameters Django-Ninja में endpoints बनाते समय उपयोग किए जाने वाले parameters के समान कार्य करते हैं, लेकिन इन्हें NinjaExtra में controller classes के साथ काम करने के लिए abstract किया गया है।

**Async Route Definition**
-----------

  
Django-Ninja-Extra में, `route` class async endpoints परिभाषित करने का support करती है, Django-Ninja के समान। यह feature Django के 3.0 से अधिक versions के लिए उपलब्ध है।

उदाहरण के लिए:

    import asyncio
    from ninja_extra import http_get, api_controller
    
    @api_controller
    class MyController:
        @http_get("/say-after")
        async def say_after(self, delay: int, word: str):
            await asyncio.sleep(delay)
            return {'saying': word}
    

  
इस illustration में, `say_after` endpoint को `async` keyword का उपयोग करके एक asynchronous function के रूप में परिभाषित किया गया है, जिससे endpoint के भीतर asynchronous operations संभव होते हैं।

  
!!! info Django-Ninja async support के बारे में अधिक पढ़ें

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
