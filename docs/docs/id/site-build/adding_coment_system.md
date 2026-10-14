---
comments: true
---
# Menambahkan Sistem Komentar Gratis Bertenaga GitHub Issues

Giscus adalah modul komentar yang ditenagai oleh sistem Discussion milik GitHub. User dapat login melalui akun GitHub mereka, dan modul ini mendukung komentar berformat Markdown. Antarmukanya bersih sekaligus menarik.

Lihat bagian bawah halaman ini untuk contohnya.

Sebelum dapat menggunakan Giscus, Anda perlu menyelesaikan langkah-langkah berikut:

## Konfigurasikan Repository Khusus untuk Giscus
*    Repository harus bersifat publik, jika tidak, pengunjung tidak akan dapat melihat discussion-nya.
*    Aplikasi giscus harus terinstal, jika tidak, pengunjung tidak akan dapat berkomentar atau merespons. [Klik di sini untuk menginstal](https://github.com/apps/giscus).
*    Fitur Discussions harus diaktifkan di repository Anda. Path untuk mengaktifkannya adalah `Settings` - `Features` - `Discussions` pada proyek.

## Hasilkan Konfigurasi Anda Secara Online
Kunjungi [Giscus](https://giscus.app/) dan gunakan tool konfigurasi mereka untuk menghasilkan snippet kode untuk memuat sistem komentar.
Salin snippet kode tersebut untuk langkah berikutnya. Snippet yang dihasilkan seharusnya terlihat mirip dengan ini.

```javascript
<script
  src="https://giscus.app/client.js"
  data-repo="<username>/<repository>"
  data-repo-id="..."
  data-category="..."
  data-category-id="..."
  data-mapping="pathname"
  data-reactions-enabled="1"
  data-emit-metadata="1"
  data-theme="light"
  data-lang="en"
  crossorigin="anonymous"
  async
>
</script>
```
## Konfigurasikan comments.html dan Letakkan di Bawah Direktori overrides/partials
comments.html (kosong secara default) adalah tempat terbaik untuk menambahkan snippet kode yang dihasilkan oleh Giscus.
Ikuti panduan ekstensi tema dan override comments.html. Ganti baris-baris yang di-highlight dengan snippet kode yang dihasilkan oleh tool konfigurasi Giscus pada langkah sebelumnya.
```hl_lines="3-17"
{% if page.meta.comments %}
  <h2 id="__comments">{{ lang.t("meta.comments") }}</h2>
  <script
      src="https://giscus.app/client.js"
      data-repo="<username>/<repository>"
      data-repo-id="..."
      data-category="..."
      data-category-id="..."
      data-mapping="pathname"
      data-reactions-enabled="1"
      data-emit-metadata="1"
      data-theme="light"
      data-lang="en"
      crossorigin="anonymous"
      async
    >
    </script>

  <!-- Synchronize Giscus theme with palette -->
  <script>
    var giscus = document.querySelector("script[src*=giscus]")

    // Set palette on initial load
    var palette = __md_get("__palette")
    if (palette && typeof palette.color === "object") {
      var theme = palette.color.scheme === "slate"
        ? "transparent_dark"
        : "light"

      // Instruct Giscus to set theme
      giscus.setAttribute("data-theme", theme) 
    }

    // Register event handlers after documented loaded
    document.addEventListener("DOMContentLoaded", function() {
      var ref = document.querySelector("[data-md-component=palette]")
      ref.addEventListener("change", function() {
        var palette = __md_get("__palette")
        if (palette && typeof palette.color === "object") {
          var theme = palette.color.scheme === "slate"
            ? "transparent_dark"
            : "light"

          // Instruct Giscus to change theme
          var frame = document.querySelector(".giscus-frame")
          frame.contentWindow.postMessage(
            { giscus: { setConfig: { theme } } },
            "https://giscus.app"
          )
        }
      })
    })
  </script>
{% endif %}
```
Struktur file:
```
.
├─ overrides/
│  └─ partials
│     └─ comments.html
│  └─ base.html
└─ mkdocs.yml
```
## Selesai

Sekarang Anda dapat mengaktifkan komentar pada sebuah halaman dengan mengatur `comments` menjadi `true` di file md:

```markdown
---
comments: true
---

# Page title
...
```


> Dokumentasi resmi: 
> 1. https://squidfunk.github.io/mkdocs-material/setup/adding-a-comment-system/?h=comment
<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
