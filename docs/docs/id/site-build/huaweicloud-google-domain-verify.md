---
comments: true
---
# Memverifikasi Kepemilikan Domain Google di Huawei Cloud

Jika Anda ingin mengaktifkan Google Analytics, Anda terlebih dahulu perlu memverifikasi kepemilikan domain.

Ada dua metode. Satu melalui URL prefix: misalnya, jika Anda memasukkan `https://pingti.ren/`, maka semua URL di bawahnya dapat dimonitor, tetapi ada kekurangannya. Subdomain tidak dapat dimonitor — misalnya, `https://docs.pingti.ren/` tidak dapat dimonitor.
Karena itu Google memiliki konsep verifikasi domain. Selama masih berhubungan dengan `pingti.ren`, semuanya dapat tercakup.

Mengenai mana yang lebih baik, itu tergantung pada kebutuhan masing-masing. Jika Anda memiliki banyak subdomain, tentu saja lebih baik memverifikasi semuanya sekaligus melalui domain.

Di sini saya akan menjelaskan cara mengisi record TXT di Huawei Cloud untuk lolos verifikasi domain Google. Praktis tidak ada informasi yang tersedia di internet; saya mencari tahu sendiri.

Kuncinya adalah memilih tipe TXT, membiarkan Name kosong, dan mengisi Value dengan kode yang diberikan Google, seperti "google-site-verification=xxxx-xxxxx". Dan harus dibungkus dengan tanda kutip. Konfigurasi lengkapnya ditunjukkan pada gambar:

!(google-site-verification)[/img/huaweicloud-google-site-verification.png]

Ini adalah metode verifikasi domain yang direkomendasikan oleh Google. Anda juga dapat melakukannya melalui CNAME, tetapi itu memerlukan dua record.

Setelah verifikasi lolos, menambahkan sitemap di konsol Google menjadi sangat fleksibel, tanpa batasan URL prefix.

!(google-console-domain-add-sitemap)[/img/google-console-domain-add-sitemap]

Seperti yang Anda lihat, sangat mudah untuk menambahkan berbagai subdomain.
