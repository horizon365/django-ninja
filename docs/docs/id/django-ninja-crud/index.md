Dokumentasi Django Ninja CRUD
=======================

![Django Ninja CRUD](../img/django-ninja-crud-cover.JPG)


Django Ninja CRUD adalah framework yang powerful, deklaratif, namun sedikit opinionated, yang menyederhanakan pengembangan endpoint CRUD (Create, Read, Update, Delete) dengan Django Ninja, dan juga menyediakan pendekatan deklaratif berbasis skenario untuk menguji endpoint-endpoint tersebut menggunakan Django REST Testing (adik dari package ini)🐣. Package ini memungkinkan Anda mendefinisikan endpoint umum sebagai class-based views dan dengan mudah mengkustomisasinya sesuai konvensi project Anda, serta dengan mudah membuat view kustom Anda sendiri dan mendeklarasikannya berdampingan dengan view CRUD yang disediakan, sehingga mendorong modularitas dan ekstensibilitas. Package ini mendorong fokus pada hal yang paling penting: menyelesaikan masalah dunia nyata, alih-alih menemukan kembali roda di seluruh project Anda.


Awalnya terinspirasi oleh ModelViewSet milik DRF, Django Ninja CRUD berevolusi untuk mengatasi keterbatasannya, mengadopsi pendekatan composition-over-inheritance untuk mencapai modularitas sejati — langkah dasar menuju antarmuka deklaratif yang lebih luas untuk membuat endpoint.


Tantangan utama dengan viewsets berbasis inheritance:

*     Keunikan endpoint CRUD per model: Django Ninja CRUD memungkinkan Anda mendefinisikan beberapa endpoint untuk model yang sama, memungkinkan versioning atau representasi alternatif.
*     Fleksibilitas kustomisasi: alih-alih meng-override metode pada satu class monolitik, masing-masing view dikustomisasi melalui composition dan konfigurasi.
*     Hubungan implisit dalam hierarki inheritance: composition memisahkan (decouple) view-view, mengurangi dependensi dan meningkatkan reusability.
*     Kurangnya modularitas untuk endpoint baru: menambahkan endpoint kustom tidak lagi memerlukan subclassing dari seluruh viewset, sehingga lebih mudah memperkenalkan fitur baru secara bertahap.

✨ Fitur Utama
-------

*     Murni deklaratif: definisikan view dan test dengan mendeklarasikan apa yang Anda inginkan, bukan bagaimana melakukannya.
*     Modularitas tak tertandingi: kustomisasi viewset dengan view CRUD yang diinginkan, mengkustomisasi perilaku setiap view.
*     Mudah di-extend: buat view kustom Anda sendiri dan gunakan sebagai komponen yang dapat digunakan kembali berdampingan dengan view CRUD yang disediakan.
*     Framework testing berbasis skenario: manfaatkan framework testing berbasis skenario untuk mendefinisikan beragam test case secara deklaratif dan ringkas.
*     Fokus pada hal yang penting: habiskan lebih banyak waktu untuk menyelesaikan masalah dunia nyata dan lebih sedikit untuk tugas-tugas umum yang repetitif.

> **
> Django Ninja CRUD lebih dari sekadar tool; ia adalah pergeseran paradigma dalam pengembangan dan testing aplikasi web Django.**

🫶 Dukungan
----------


Pertama-tama, terima kasih setulus-tulusnya kepada 400+ stargazers yang telah mendukung project ini. Pengakuan dan kepercayaan Anda terhadap potensinya memotivasi saya untuk terus memelihara dan meningkatkan karya ini, membuatnya lebih terlihat oleh calon user dan kontributor baru.

[![Star History Chart](https://api.star-history.com/svg?repos=hbakri/django-ninja-crud&type=Date)](https://star-history.com/#hbakri/django-ninja-crud&Date)


Jika Anda telah memperoleh manfaat dari project ini atau menghargai dedikasi di baliknya, pertimbangkan untuk memberikan dukungan lebih lanjut. Baik seharga segelas kopi, sepatah kata penyemangat, atau sebuah sponsorship, setiap gestur menambah kayu bakar bagi api open source dan membuatnya bersinar lebih terang.✨

[![Sponsor](https://img.shields.io/badge/sponsor-donate-pink?logo=github-sponsors&logoColor=white)](https://github.com/sponsors/hbakri) [![Buy me a coffee](https://img.shields.io/badge/buy_me_a_coffee-donate-pink?logo=buy-me-a-coffee&logoColor=white)](https://www.buymeacoffee.com/hbakri)


Kebaikan dan dukungan Anda sangat berarti. Terima kasih!🙏
