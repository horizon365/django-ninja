**Panduan Kontribusi**
=========
  
Terima kasih telah mempertimbangkan untuk berkontribusi pada NinjaExtra! Kontribusi Anda membantu membuat project ini lebih baik untuk semua orang. Sebelum memulai, mohon luangkan waktu sejenak untuk meninjau panduan-panduan berikut.

  
Menyiapkan Lingkungan Pengembangan
---------

1.    
    Fork repositori: Fork repositori NinjaExtra di GitHub dan clone secara lokal.
    
2.    
    Virtual environment: Buat dan aktifkan virtual environment untuk project tersebut.
    
        python -m venv venv
        source venv/bin/activate  # Linux/macOS
        
    
        python -m venv venv
        .\venv\Scripts\activate  # Windows
        
    
3.    
    Install `flit`: Pastikan `flit` terinstall secara global.
    
        pip install flit
        
    
4.    
    Install dependensi: Install library pengembangan dan pre-commit hooks.
    
        make install-full
        

### **Gaya Kode dan Formatting**

*     
    Formatting: Untuk memformat kode dan memastikan konsistensi, jalankan:
    
        make fmt
        
    
*     
    Linting: NinjaExtra menggunakan `mypy` dan `ruff` untuk linting. Jalankan perintah berikut untuk memeriksa sintaks kode:
    
        make lint
        

### **Testing**

*     
    Unit test: Kami menggunakan `pytest` untuk unit testing. Jalankan test suite:
    
        make test
        
    
*     
    Test coverage: Untuk memeriksa test coverage:
    
        make test-cov
        

### **Mengirimkan Pull Request**

1.    
    Branch: Buat branch baru untuk fitur atau perbaikan bug Anda.
    
        git checkout -b feature-branch
        
    
2.    
    Pesan commit: Ikuti spesifikasi conventional commit untuk pesan commit.
    
3.    
    Push perubahan: Push branch Anda ke repositori hasil fork Anda.
    
        git push origin feature-branch
        
    
4.    
    Pull request: Buka sebuah pull request ke branch `master` dari repositori NinjaExtra. Berikan judul dan deskripsi yang jelas untuk perubahan Anda.
    

  
Terima kasih telah berkontribusi di NinjaExtra! 🚀

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
