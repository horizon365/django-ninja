**Izin (Permission) API Controller**
================

  
Konsep sistem permission bersumber dari Django DRF.

  
Pemeriksaan permission selalu dijalankan pada awal fungsi route, sebelum kode lain diizinkan untuk melanjutkan. Pemeriksaan permission biasanya akan menggunakan informasi autentikasi di atribut `request.user` dan `request.auth` untuk menentukan apakah request yang masuk diizinkan atau tidak.

  
Permission digunakan untuk memberikan atau menolak akses ke bagian-bagian berbeda dari API untuk kelas user yang berbeda.

  
Gaya permission yang paling sederhana adalah mengizinkan akses bagi user yang terautentikasi dan menolak akses bagi user yang tidak terautentikasi. Ini sesuai dengan class `IsAuthenticated` di Django Ninja Extra.

  
Gaya permission yang sedikit tidak terlalu ketat adalah memberikan akses penuh bagi user terautentikasi dan akses read-only bagi user yang tidak terautentikasi. Ini sesuai dengan class `IsAuthenticatedOrReadOnly` di Django Ninja Extra.

### **Keterbatasan Permission Tingkat Objek**

  
Saat menangani request, metode `has_permission` otomatis dipanggil untuk semua permission yang ditentukan dalam daftar permission fungsi route. Namun, karena `has_object_permission` membutuhkan sebuah objek untuk validasi permission, metode tersebut tidak terpicu. Oleh karena itu, saat menggunakan metode `get_object_or_exception` atau `get_object_or_none` di sebuah controller untuk mengambil objek, metode permission `has_object_permission` akan dipanggil.

**Permission Kustom**
----------

  
Untuk mengimplementasikan permission kustom, override `BasePermission` dan implementasikan salah satu atau kedua metode berikut:

    .has_permission(self, request: HttpRequest, controller: "APIController")
    .has_object_permission(self, request: HttpRequest, controller: "APIController", obj: Any)
    

Contoh

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
Operator Permission yang Didukung**
---------------

*   & (and) contoh: `permissions.IsAuthenticated & ReadOnly`
*   | (or) contoh: `permissions.IsAuthenticated | ReadOnly`
*   ~ (not) contoh: `~(permissions.IsAuthenticated & ReadOnly)`

**  
Menggunakan Objek Permission di Controller**
------------------

  
Sistem permission Ninja-Extra memberikan fleksibilitas saat mendefinisikan permission, memungkinkan permission didefinisikan sebagai instance atau tipe dari class permission.

  
Pada contoh di bawah, class `ReadOnly` didefinisikan sebagai subclass dari `permissions.BasePermission`, dan instance-nya kemudian diberikan ke parameter `permissions` di decorator `api_controller`.

    from ninja_extra import permissions, api_controller, ControllerBase
    
    class ReadOnly(permissions.BasePermission):
        def has_permission(self, request, view):
            return request.method in permissions.SAFE_METHODS
    
    @api_controller(permissions=[permissions.IsAuthenticated | ReadOnly()])
    class SampleController(ControllerBase):
        pass
    

  
Pada contoh yang diberikan, class `UserWithPermission` digunakan untuk mengevaluasi permission yang berbeda untuk controller atau fungsi route yang berbeda.

Misalnya:

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
    

  
Dalam kasus ini, class `UserWithPermission` digunakan untuk memverifikasi apakah user memiliki permission `blog.add` untuk mengakses action `add_blog` dan permission `blog.delete` untuk mengakses action `delete_blog`. Permission dikonfigurasikan secara eksplisit untuk setiap fungsi route agar memungkinkan kontrol akses user yang granular berdasarkan permission tertentu.

**AllowAny**
------------

  
Class permission `AllowAny` memberikan akses tanpa batasan, terlepas dari apakah request terautentikasi atau tidak. Meskipun tidak diwajibkan, penggunaan class permission ini bersifat opsional karena Anda dapat mencapai hasil yang sama dengan mengatur permissions menjadi list atau tuple kosong. Namun, menentukan class `AllowAny` bisa membantu karena secara jelas menyampaikan maksud untuk mengizinkan akses tanpa batasan.

**IsAuthenticated**
-------------

  
Class permission `IsAuthenticated` menolak permission bagi user yang tidak terautentikasi dan memberikan permission bagi user yang terautentikasi.

  
Jika Anda berniat membatasi akses API hanya untuk user yang terdaftar, permission ini yang tepat.

**IsAdminUser**
---------------

  
Class permission `IsAdminUser` menolak permission bagi user mana pun kecuali `user.is_staff` bernilai `True`, dalam hal mana permission diberikan.

  
Jika Anda berniat membatasi akses API hanya untuk subset administrator terpercaya tertentu, permission ini yang tepat.

**  
IsAuthenticatedOrReadOnly**
---------------

  
Class permission `IsAuthenticatedOrReadOnly` mengizinkan user terautentikasi melakukan request apa pun. Bagi user yang tidak terautentikasi, request hanya diizinkan ketika metodenya termasuk metode "safe" (yaitu, GET, HEAD, atau OPTIONS).

  
Jika Anda ingin API Anda memberikan permission baca kepada user anonim sambil membatasi permission tulis hanya untuk user terautentikasi, permission ini yang tepat.
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
