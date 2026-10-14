# Token Authentication Django Ninja dengan Djoser


Source URL: https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser


Chinese content: This question shows research effort; it is useful and clear

2

Simpan pertanyaan ini.

[](https://stackoverflow.com/posts/70716976/timeline)


Show activity on this post.


Saya telah mengimplementasikan CRUD menggunakan framework Django Ninja, tetapi sekarang saya ingin melakukan autentikasi di aplikasi saya. Saya telah menginstall dan mengonfigurasi Djoser, jadi sekarang saya bisa menghasilkan token, tetapi saya tidak tahu bagaimana memverifikasinya di CRUD saya

    class AuthBearer(HttpBearer):
        def authenticate(self, request, token):
            if token == "supersecret":
                return token
    
    @api.get("/bearer", auth=AuthBearer())
    def bearer(request):
        return {"token": request.auth}



Saya seharusnya bisa memeriksa token di fungsi "AuthBearer", tetapi saya tidak tahu caranya

repo saya ([link](https://github.com/arsalanses/ham-radio-logger/blob/master/logs/api/v1.py))

*   [django](https://stackoverflow.com/questions/tagged/django "show questions tagged 'django'")
*   [django-rest-framework](https://stackoverflow.com/questions/tagged/django-rest-framework "show questions tagged 'django-rest-framework'")
*   [djoser](https://stackoverflow.com/questions/tagged/djoser "show questions tagged 'djoser'")
*   [django-ninja](https://stackoverflow.com/questions/tagged/django-ninja "show questions tagged 'django-ninja'")

[Bagikan](https://stackoverflow.com/q/70716976 "Short permalink to this question")


Bagikan link ke pertanyaan ini

Copy link[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/ "The current license for this post: CC BY-SA 4.0")

[Perbaiki pertanyaan ini](https://stackoverflow.com/posts/70716976/edit)

Follow


Follow this question to receive notifications

[diedit Dec 8, 2022 pukul 17:18](https://stackoverflow.com/posts/70716976/revisions "show all edits to this post")

[![Image 1: metersk's user avatar](https://www.gravatar.com/avatar/f1a23a45808b0429be1543ca726d522f?s=64&d=identicon&r=PG)](https://stackoverflow.com/users/1887261/metersk)

[metersk](https://stackoverflow.com/users/1887261/metersk)

12.3k2222 gold badges6868 silver badges103103 bronze badges


Ditanyakan Jan 14, 2022 pukul 21:59

[![Image 2: Arsalan's user avatar](https://i.sstatic.net/R9DYa.jpg?s=64)](https://stackoverflow.com/users/3711191/arsalan)

[Arsalan](https://stackoverflow.com/users/3711191/arsalan)Arsalan

7722 silver badges99 bronze badges

[Tambahkan komentar](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Use comments to ask for more information or suggest improvements. Avoid answering questions in comments.") |[](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Expand to show all comments on this post")

1 Jawaban 1
----------


Urutkan: Reset ke default


Skor tertinggi (default) Trending (vote terbaru dihitung lebih banyak) Tanggal dimodifikasi (terbaru dulu) Tanggal dibuat (terbaru dulu)


Jawaban ini berguna

6

Simpan jawaban ini.

[](https://stackoverflow.com/posts/70720995/timeline)


Show activity on this post.


Jadi pada dasarnya Anda harus meng-extend class HttpBearer milik Ninja dan mengimplementasikan metode authenticate, yang akan menerima request dan token sebagai argumen. Metode ini akan mengembalikan None jika user tidak terautentikasi, atau sebuah string yang akan diisi ke request.auth jika user terautentikasi. Biasanya, string ini adalah username, sehingga Anda dapat menggunakannya di semua endpoint. Kurang lebih seperti ini (saya menggunakan PyJWT untuk mendecode token):

    import jwt
    from ninja.security import HttpBearer
    
    class AuthBearer(HttpBearer):
        def authenticate(self, request, token):
            try:
                #JWT secret key is set up in settings.py
                JWT_SIGNING_KEY = getattr(settings, "JWT_SIGNING_KEY", None)
                payload = jwt.decode(token, JWT_SIGNING_KEY, algorithms=["HS256"])
                username: str = payload.get("sub")
                if username is None:
                    return None
            except jwt.PyJWTError as e:
                return None
    
            return username


[Bagikan](https://stackoverflow.com/a/70720995 "Short permalink to this answer")


Bagikan link ke jawaban ini

Copy link[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/ "The current license for this post: CC BY-SA 4.0")

[Perbaiki jawaban ini](https://stackoverflow.com/posts/70720995/edit)

Follow


Follow this answer to receive notifications


Dijawab Jan 15, 2022 pukul 11:30 AM

[![Image 3: abolfazlmalekahmadi's user avatar](https://i.sstatic.net/CeWmU.png?s=64)](https://stackoverflow.com/users/10356618/abolfazlmalekahmadi)

[abolfazlmalekahmadi](https://stackoverflow.com/users/10356618/abolfazlmalekahmadi)abolfazlmalekahmadi

26822 silver badges1717 bronze badges

1

* Terima kasih untuk contoh kodenya! Bagaimana Anda menghasilkan token yang ter-encode? Apakah Anda menyimpan token-token ini di storage?

  –[netcyrax](https://stackoverflow.com/users/2456568/netcyrax "1,089 reputation")

  [  
  Dikomentari Jul 18, 2023 pukul 9:29](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser#comment135243481_70720995)

[Tambahkan komentar](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Use comments to ask for more information or suggest improvements. Avoid comments like “+1” or “thanks”.") |[](https://stackoverflow.com/questions/70716976/django-ninja-token-authentication-with-djoser# "Expand to show all comments on this post")

@media (prefers-color-scheme: dark) { body { color: #fff !important; background-color: #272727 !important; } } body { overflow-y: hidden; }
