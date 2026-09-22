# Sistem Manajemen Parkir Kendaraan (CLI OOP)

## 1. Penjelasan Program
Program ini adalah aplikasi antarmuka baris perintah (CLI) berbasis Object-Oriented Programming (OOP) yang dirancang untuk mengelola alur masuk dan keluar kendaraan pada suatu area parkir. Sistem beroperasi secara interaktif menggunakan mekanisme CRUD (Create, Read, Update, Delete) untuk mendaftarkan kendaraan baru, memantau kendaraan yang sedang terparkir, memproses pelunasan karcis, hingga menghapus data saat kendaraan meninggalkan area. Seluruh memori operasional, termasuk sisa kuota parkir dan akumulasi saldo, secara otomatis disinkronkan ke dalam file `transaksi_parkir.csv` dan `status_area.csv` agar data tidak hilang ketika program dimatikan.

## 2. Struktur Class
Pada langkah ini, dilakukan pendefinisian class `AreaParkir` yang berfungsi mengelola data pusat meliputi identitas lokasi, batas kapasitas maksimal, dan akumulasi total pendapatan harian. Class ini menerapkan enkapsulasi mutlak pada atribut pendapatan melalui mekanisme properti pembaca (getter) dan pembaru (setter), di mana sistem validasi internal akan langsung membangkitkan eksepsi `ValueError` apabila sistem mencoba memasukkan nilai nominal yang bersifat negatif. Interaksi pelacakan ketersediaan ruang parkir didukung oleh fungsi utilitas statis tanpa harus memanggil nilai spesifik dari dalam objek.

Pada langkah ini, dilakukan perancangan class `Kendaraan` untuk merekam entitas fisik secara spesifik dengan menyimpan atribut jenis kendaraan dan plat nomor. Atribut plat nomor disembunyikan menggunakan pembatas akses privat, yang jalur modifikasinya dikunci menggunakan aturan validasi ketat untuk menolak instruksi perubahan apabila teks yang dimasukkan kosong atau panjang karakternya tidak mencapai batas minimum empat digit. Pembuatan objek baru dipermudah oleh keberadaan fungsi pabrik atau class method yang bertugas membongkar input teks mentah bersimbol koma menjadi data parameter yang siap dikonstruksi.

Pada langkah ini, dilakukan penyusunan class `KarcisParkir` sebagai komponen relasional yang merajut objek fisik kendaraan dengan sistem administrasi dan transaksi keuangan. Variabel privat digunakan secara eksklusif untuk menyimpan status pelunasan tiket guna menghindari peretasan logika, didukung oleh validasi bertipe bawaan yang memblokir semua masukan di luar format logika kebenaran boolean (True/False). Rekaman transaksi pada objek ini kemudian diekstrak dan didistribusikan ke dalam penyimpan berkas koma (CSV) menggunakan fungsi utilitas khusus.

## 3. Panduan Pengujian

### A. Skenario Pendaftaran Kendaraan (Create & Validasi)
1. Jalankan program dan ketik angka `1` pada menu utama.
2. Uji sistem validasi dengan memasukkan data yang salah: ketik `Truk, KT 123` lalu tekan Enter. Sistem harus menolak input karena "Truk" bukan jenis yang diizinkan dan panjang plat nomor kurang dari standar.
3. Masukkan data yang benar: ketik `Mobil, KT 1234 XX`. Sistem akan menerima masukan, mengurangi sisa kuota parkir, dan mencetak tiket dengan ID baru (misal: SMD-0001).

### B. Skenario Pemantauan Data (Read)
1. Pilih menu nomor `2`.
2. Program akan menampilkan seluruh kendaraan yang status karcisnya masih berada di dalam area parkir. Pastikan karcis SMD-0001 muncul dengan status "BELUM LUNAS".

### C. Skenario Pembayaran (Update & Logika Keuangan)
1. Pilih menu nomor `3` untuk memperbarui data.
2. Masukkan ID Karcis `SMD-0001`, kemudian pilih opsi `b` (Status Lunas).
3. Konfirmasi pembayaran dengan mengetik `Y`.
4. Untuk membuktikan sistem pelunasan berhasil menambah saldo, kembali ke menu utama lalu pilih angka `5` (Lihat Rekap Area). Total Pendapatan harus bertambah sebesar Rp5.000 (tarif dasar mobil).

### D. Skenario Kendaraan Keluar (Delete)
1. Pilih menu nomor `4`.
2. Masukkan ID Karcis `SMD-0001`. Program akan menghapus karcis dari dalam dictionary karena statusnya sudah tervalidasi lunas.
3. Jika menu `5` dibuka kembali, jumlah "Kendaraan Aktif" akan berkurang kembali ke angka 0, menandakan sistem telah membebaskan slot ruang parkir tersebut untuk pelanggan berikutnya.