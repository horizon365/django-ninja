
Beberapa perilaku Ninja JWT dapat dikustomisasi melalui variabel pengaturan di `settings.py`:

```python
# Django project settings.py

from datetime import timedelta
from django.conf import settings
...

NINJA_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': settings.SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'ninja_jwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('ninja_jwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'ninja_jwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    
    # For Controller Schemas
    # FOR OBTAIN PAIR
    'TOKEN_OBTAIN_PAIR_INPUT_SCHEMA': "ninja_jwt.schema.TokenObtainPairInputSchema",
    'TOKEN_OBTAIN_PAIR_REFRESH_INPUT_SCHEMA': "ninja_jwt.schema.TokenRefreshInputSchema",
    # FOR SLIDING TOKEN
    'TOKEN_OBTAIN_SLIDING_INPUT_SCHEMA': "ninja_jwt.schema.TokenObtainSlidingInputSchema",
    'TOKEN_OBTAIN_SLIDING_REFRESH_INPUT_SCHEMA':"ninja_jwt.schema.TokenRefreshSlidingInputSchema",
    
    'TOKEN_BLACKLIST_INPUT_SCHEMA': "ninja_jwt.schema.TokenBlacklistInputSchema",
    'TOKEN_VERIFY_INPUT_SCHEMA': "ninja_jwt.schema.TokenVerifyInputSchema",
}
```

Di atas, ditampilkan nilai default dari pengaturan-pengaturan tersebut.

## `ACCESS_TOKEN_LIFETIME`

Objek `datetime.timedelta` yang menentukan masa berlaku (lifetime) dari access token.
Saat pembuatan token, nilai `timedelta` ini ditambahkan ke waktu UTC saat ini untuk memperoleh nilai default claim `exp` dari token.

## `REFRESH_TOKEN_LIFETIME`

Objek `datetime.timedelta` yang menentukan masa berlaku (lifetime) dari refresh token.
Saat pembuatan token, nilai `timedelta` ini ditambahkan ke waktu UTC saat ini untuk memperoleh nilai default claim `exp` dari token.

### ``BLACKLIST_AFTER_ROTATION``
----------------------------
Ketika diatur ke ``True``, jika blacklist app sedang digunakan dan ``ROTATE_REFRESH_TOKENS`` diatur ke ``True``,
refresh token yang dikirimkan ke ``TokenRefreshView`` akan ditambahkan ke blacklist.
Anda perlu menambahkan ``'ninja_jwt.token_blacklist'`` ke ``INSTALLED_APPS`` di file pengaturan Anda untuk menggunakan setting ini.


Pelajari lebih lanjut tentang `/blacklist_app`{.interpreted-text role="doc"}.

## `UPDATE_LAST_LOGIN`

Ketika diatur ke `True`, field last_login di tabel auth_user akan diperbarui saat login (TokenObtainPairView).

    Peringatan: Memperbarui last login akan sangat meningkatkan jumlah transaksi database.
    Penyalahgunaan view ini dapat memperlambat server, yang dapat menjadi celah keamanan.
    Jika Anda benar-benar ingin melakukannya, setidaknya lakukan throttle pada endpoint tersebut dengan DRF.

## `ALGORITHM`

Algoritma dari library PyJWT yang digunakan untuk melakukan operasi signing/verification pada token.
Untuk menggunakan signing dan verification HMAC simetris, Anda dapat menggunakan algoritma berikut: ``'HS256'``, ``'HS384'``,``'HS512'``.
Saat memilih algoritma HMAC, setting ``SIGNING_KEY`` akan digunakan sebagai signing key sekaligus verification key.
Dalam hal ini, setting ``VERIFYING_KEY`` diabaikan.
Untuk menggunakan signing dan verification RSA asimetris, Anda dapat menggunakan algoritma berikut: ``'RS256'``, ``'RS384'``, ``'RS512'``.
Saat memilih algoritma RSA, setting ``SIGNING_KEY`` harus diatur ke string yang berisi RSA private key.
Demikian pula, setting ``VERIFYING_KEY`` harus diatur ke string yang berisi RSA public key.

## `SIGNING_KEY`

Signing key yang digunakan untuk menandatangani konten token yang dihasilkan.
Untuk signing HMAC, ini harus berupa string acak dengan jumlah bit data setidaknya sebanyak yang dibutuhkan oleh protokol signing yang digunakan.
Untuk signing RSA, ini harus berupa string yang berisi RSA private key dengan panjang 2048 bit atau lebih.
Karena Simple JWT menggunakan signing HMAC 256-bit secara default, setting `SIGNING_KEY` secara default menggunakan nilai dari setting `SECRET_KEY` proyek Django Anda.
Meskipun ini adalah default yang paling masuk akal yang dapat diberikan oleh Simple JWT, disarankan agar developer mengubah setting ini menjadi nilai yang independen dari secret key proyek Django.
Hal ini akan memudahkan penggantian signing key apabila signing key yang digunakan untuk token mengalami kebocoran.

## `VERIFYING_KEY`

Verification key yang digunakan untuk memverifikasi konten token yang dihasilkan. Jika setting ``ALGORITHM`` menentukan algoritma HMAC,
setting ``VERIFYING_KEY`` diabaikan dan nilai dari ``SIGNING_KEY`` yang digunakan sebagai gantinya.
Jika setting ``ALGORITHM`` menentukan algoritma RSA, setting ``VERIFYING_KEY`` harus diatur ke string yang berisi RSA public key.

## `AUDIENCE`

Claim audience yang akan disertakan dalam token yang dihasilkan dan/atau diverifikasi pada token yang di-decode.
Ketika diatur ke ``None``, field ini dikecualikan dari token dan tidak diverifikasi.

## `ISSUER`

Claim issuer yang akan disertakan dalam token yang dihasilkan dan/atau diverifikasi pada token yang di-decode.
Ketika diatur ke ``None``, field ini dikecualikan dari token dan tidak diverifikasi.

### ``JWK_URL``
----------

JWK_URL digunakan untuk menyelesaikan (resolve) public key yang dibutuhkan untuk memverifikasi signature token secara dinamis.
Sebagai contoh, saat menggunakan Auth0, Anda mungkin mengatur ini ke 'https://yourdomain.auth0.com/.well-known/jwks.json'.
Ketika diatur ke ``None``, field ini dikecualikan dari token backend dan tidak digunakan saat verifikasi

### ``LEEWAY``
----------

Leeway digunakan untuk memberikan sejumlah margin terhadap waktu kedaluwarsa. Ini dapat berupa bilangan bulat detik atau ``datetime.timedelta``.
Silakan merujuk ke https://pyjwt.readthedocs.io/en/latest/usage.html#expiration-time-claim-exp untuk informasi lebih lanjut.

###``AUTH_HEADER_TYPES``
---------------------

Tipe header otorisasi yang akan diterima untuk views yang membutuhkan autentikasi. Sebagai contoh, nilai ``'Bearer'`` berarti views yang membutuhkan autentikasi akan mencari header dengan format berikut:
``Authorization: Bearer <token>``. Setting ini juga dapat berisi list atau tuple dari beberapa kemungkinan tipe header (misalnya ``('Bearer', 'JWT')``).
Jika list atau tuple digunakan dengan cara ini, dan autentikasi gagal, item pertama dalam koleksi tersebut akan digunakan untuk menyusun header "WWW-Authenticate" pada response.

###``AUTH_HEADER_NAME``
----------------------------

Nama header otorisasi yang digunakan untuk autentikasi. Nilai defaultnya adalah `HTTP_AUTHORIZATION`, yang akan menerima header `Authorization` dari request.
Sebagai contoh, jika Anda ingin menggunakan `X_Access_Token` pada header request Anda, tentukan `AUTH_HEADER_NAME` sebagai `HTTP_X_ACCESS_TOKEN` di pengaturan Anda.


###``USER_ID_FIELD``
-----------------

Field database pada model user yang akan disertakan dalam token yang dihasilkan untuk mengidentifikasi user.
Disarankan agar nilai setting ini menentukan field yang biasanya tidak berubah setelah nilai awalnya dipilih.
Sebagai contoh, menentukan field "username" atau "email" merupakan pilihan yang kurang baik,
karena username atau email sebuah akun dapat berubah tergantung pada bagaimana manajemen akun dirancang pada suatu layanan.
Hal ini dapat memungkinkan akun baru dibuat dengan username lama, sementara token yang sudah ada yang menggunakan username tersebut sebagai identifier user tetap valid.

###``USER_ID_CLAIM``
-----------------

Claim yang digunakan untuk menyimpan identifier user dalam token yang dihasilkan. Sebagai contoh, mengatur nilai menjadi ```"user_id"``` berarti token yang dihasilkan mengandung claim "user_id",
yang berisi identifier user tersebut.

###``USER_AUTHENTICATION_RULE``
----------------------------

Callable yang digunakan untuk menentukan apakah user diizinkan untuk terautentikasi. Rule ini diterapkan setelah token yang valid diproses. Objek user diteruskan sebagai argumen ke callable tersebut.
Rule default-nya adalah memeriksa bahwa flag ``is_active`` masih ``True``.
Callable tersebut harus mengembalikan nilai boolean, ``True`` berarti diizinkan, jika tidak ``False`` yang menghasilkan status code 401.

###``AUTH_TOKEN_CLASSES``
----------------------

Daftar dotted path yang menunjuk ke kelas-kelas yang menentukan tipe token yang diizinkan untuk membuktikan autentikasi. Informasi lebih lanjut ada di bagian "Token Types" di bawah.

###``TOKEN_TYPE_CLAIM``
--------------------

Nama claim yang digunakan untuk menyimpan tipe token. Informasi lebih lanjut ada di bagian "Token Types" di bawah.

###``JTI_CLAIM``
-------------

Nama claim yang digunakan untuk menyimpan identifier unik token. Identifier ini digunakan untuk mengidentifikasi token yang dicabut (revoked) pada blacklist app.
Dalam beberapa kasus, mungkin diperlukan claim selain claim "jti" default untuk menyimpan nilai tersebut.

###``TOKEN_USER_CLASS``
--------------------

Objek user stateless yang didukung oleh token terverifikasi. Hanya digunakan oleh backend autentikasi JWTStatelessUser.
Nilainya adalah dotted path yang menunjuk ke subclass Anda dari ``"rest_framework_simplejwt.models.TokenUser"``, yang juga merupakan nilai default-nya.

###``SLIDING_TOKEN_LIFETIME``
--------------------------

Objek ``datetime.timedelta`` yang menentukan berapa lama sliding token valid untuk membuktikan autentikasi.
Saat pembuatan token, nilai ``timedelta`` ini ditambahkan ke waktu UTC saat ini untuk memperoleh nilai default claim "exp" dari token.
Informasi lebih lanjut ada di bagian "Sliding Tokens" di bawah.

###``SLIDING_TOKEN_REFRESH_LIFETIME``
----------------------------------

Objek ``datetime.timedelta`` yang menentukan berapa lama sliding token valid untuk di-refresh.
Saat pembuatan token, nilai `timedelta` ini ditambahkan ke waktu UTC saat ini untuk memperoleh nilai default claim "exp" dari token.
Informasi lebih lanjut ada di bagian "Sliding Tokens" di bawah.

###``SLIDING_TOKEN_REFRESH_EXP_CLAIM``
-----------------------------------

Nama claim yang digunakan untuk menyimpan waktu kedaluwarsa dari periode refresh sliding token. Informasi lebih lanjut ada di bagian "Sliding Tokens" di bawah.

!!! success

    Lanjutkan ke bab berikutnya **[Mengustomisasi Token Claim](customizing_token_claims.md)**.

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
