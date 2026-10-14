**API Controller Permissions**
================

  
Permission system की अवधारणा Django DRF से ली गई है।

  
Permission checks हमेशा route function की शुरुआत में चलते हैं, किसी अन्य कोड के चलने से पहले। Permission checks आमतौर पर यह निर्धारित करने के लिए `request.user` और `request.auth` attributes में उपलब्ध authentication information का उपयोग करते हैं कि क्या incoming request को अनुमति दी जानी चाहिए।

  
Permissions का उपयोग API के विभिन्न हिस्सों तक विभिन्न प्रकार के users के लिए access प्रदान करने या अस्वीकार करने के लिए किया जाता है।

  
सबसे सरल permission style किसी भी authenticated user को access देना और किसी भी unauthenticated user को access अस्वीकार करना है। यह Django Ninja Extra में `IsAuthenticated` class के अनुरूप है।

  
एक थोड़ा कम strict permission style है authenticated users को पूर्ण access देना और unauthenticated users को read-only access देना। यह Django Ninja Extra में `IsAuthenticatedOrReadOnly` class के अनुरूप है।

### **Object-Level Permissions की सीमाएँ**

  
Request को handle करते समय, route function की permission list में निर्दिष्ट सभी permissions के लिए `has_permission` method स्वचालित रूप से call किया जाता है। हालाँकि, चूँकि `has_object_permission` को permission validation के लिए एक object की आवश्यकता होती है, इसलिए इसे trigger नहीं किया जाता। इसलिए, किसी controller में कोई object प्राप्त करने के लिए `get_object_or_exception` या `get_object_or_none` methods का उपयोग करते समय, `has_object_permission` permission method को call किया जाएगा।

**Custom Permissions**
----------

  
एक custom permission implement करने के लिए, `BasePermission` को override करें और निम्नलिखित methods में से एक या दोनों implement करें:

    .has_permission(self, request: HttpRequest, controller: "APIController")
    .has_object_permission(self, request: HttpRequest, controller: "APIController", obj: Any)
    

उदाहरण

    from ninja_extra import permissions, api_controller, http_get
    
    class ReadOnly(permissions.BasePermission):
        def has_permission(self, request, view):
            return request.method in permissions.SAFE_METHODS
    
    @api_controller(permissions=[permissions.IsAuthenticated | ReadOnly])
    class PermissionController:
        @http_get('/must_be_authenticated', permissions=[permissions.IsAuthenticated])
        def must_be_authenticated(self, word: str):
            return dict(says=word)
    

**  
समर्थित Permission Operators**
---------------

*   & (and) जैसे: `permissions.IsAuthenticated & ReadOnly`
*   | (or) जैसे: `permissions.IsAuthenticated | ReadOnly`
*   ~ (not) जैसे: `~(permissions.IsAuthenticated & ReadOnly)`

**  
Controllers में Permission Objects का उपयोग करना**
------------------

  
Ninja-Extra permission system permissions परिभाषित करते समय flexibility प्रदान करता है, जिससे permissions को permission classes के instances या types दोनों के रूप में परिभाषित किया जा सकता है।

  
नीचे दिए गए उदाहरण में, `ReadOnly` class को `permissions.BasePermission` का एक subclass परिभाषित किया गया है, और फिर इसका instance `api_controller` decorator में `permissions` parameter को पास किया जाता है।

    from ninja_extra import permissions, api_controller, ControllerBase
    
    class ReadOnly(permissions.BasePermission):
        def has_permission(self, request, view):
            return request.method in permissions.SAFE_METHODS
    
    @api_controller(permissions=[permissions.IsAuthenticated | ReadOnly()])
    class SampleController(ControllerBase):
        pass
    

  
दिए गए उदाहरण में, `UserWithPermission` class का उपयोग विभिन्न controllers या route functions के लिए विभिन्न permissions का मूल्यांकन करने के लिए किया जाता है।

उदाहरण के लिए:

    from ninja_extra import permissions, api_controller, ControllerBase, http_post, http_delete
    
    class UserWithPermission(permissions.BasePermission):
        def __init__(self, permission: str) -> None:
            self._permission = permission
        
        def has_permission(self, request, view):
            return request.user.has_perm(self._permission)
    
    
    @api_controller('/blog')
    class BlogController(ControllerBase):
        @http_post('/', permissions=[permissions.IsAuthenticated & UserWithPermission('blog.add')])
        def add_blog(self):
            pass
        
        @http_delete('/', permissions=[permissions.IsAuthenticated & UserWithPermission('blog.delete')])
        def delete_blog(self):
            pass
    

  
इस मामले में, `UserWithPermission` class का उपयोग यह सत्यापित करने के लिए किया जाता है कि क्या user के पास `add_blog` action तक पहुँचने के लिए `blog.add` permission है और `delete_blog` action तक पहुँचने के लिए `blog.delete` permission है। User access को specific permissions के आधार पर fine-grained control के लिए प्रत्येक route function के लिए permissions स्पष्ट रूप से configure की जाती हैं।

**AllowAny**
------------

  
`AllowAny` permission class बिना किसी प्रतिबंध के access प्रदान करती है, चाहे request authenticated हो या नहो। हालाँकि इसकी आवश्यकता नहीं है, इस permission class का उपयोग करना वैकल्पिक है क्योंकि आप permissions को एक खाली list या tuple सेट करके भी वही परिणाम प्राप्त कर सकते हैं। फिर भी, `AllowAny` class निर्दिष्ट करना सहायक हो सकता है क्योंकि यह स्पष्ट रूप से बिना प्रतिबंध access देने के इरादे को व्यक्त करती है।

**IsAuthenticated**
-------------

  
`IsAuthenticated` permission class unauthenticated users को permissions अस्वीकार करती है और authenticated users को permissions प्रदान करती है।

  
यदि आप API access केवल registered users तक सीमित करना चाहते हैं, तो यह permission उपयुक्त है।

**IsAdminUser**
---------------

  
`IsAdminUser` permission class किसी भी user को permissions अस्वीकार करती है जब तक कि `user.is_staff` `True` न हो, जिस स्थिति में permission प्रदान की जाती है।

  
यदि आप API access को trusted administrators के एक specific subset तक सीमित करना चाहते हैं, तो यह permission उपयुक्त है।

**  
IsAuthenticatedOrReadOnly**
---------------

  
`IsAuthenticatedOrReadOnly` permission class authenticated users को कोई भी request करने की अनुमति देती है। Unauthenticated users के लिए, request केवल तब अनुमति दी जाती है जब method "safe" methods में से एक हो (अर्थात, GET, HEAD, या OPTIONS)।

  
यदि आप चाहते हैं कि आपकी API anonymous users को read permissions प्रदान करे जबकि write permissions को authenticated users तक सीमित रखे, तो यह permission उपयुक्त है।
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
