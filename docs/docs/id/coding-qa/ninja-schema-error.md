`ninja_schema` dan schema di dalam `ninja` terasa sangat berbeda — milik ninja berfungsi, tetapi yang di `ninja_schema` muncul error
==========================================================

A: Apakah `ninja_schema` sebuah package terpisah?
B: Ya, perlu di-install via pip. Saya melihat source code-nya, sepertinya ia menarik beberapa hal dari pydantic. Tetapi saya tidak paham pydantic, jadi saya tidak yakin persisnya fungsionalitas apa yang diimplementasikan oleh hal-hal yang baru ditambahkan itu.

A: Menurut saya schema milik ninja sudah lebih dari cukup.
B: Untuk meratakan (flatten) output foreign key, di dokumentasi digunakan seperti ini: `owner_first_name: str = Field(None, alias="owner.first_name")`
B: Menggunakan yang dari `ninja_schema` terus-menerus muncul error, katanya input seharusnya `str`, tetapi yang diberikan adalah objek.
B: Saya tidak pernah menyangka bahwa `Schema` dari `ninja_schema` inilah penyebabnya.
