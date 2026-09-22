# class MesinATM:
#     def __init__(self, id_atm, lokasi, saldo_kas):
#         self.id_atm = id_atm
#         self.lokasi = lokasi
#         self.saldo_kas = saldo_kas

#     def proses_penarikan(self, nama_nasabah, jumlah):
#         if jumlah <= self.saldo_kas:
#             self.saldo_kas -= jumlah
#             print(f" [ATM {self.id_atm}] Penarikan Rp{jumlah:,} oleh {nama_nasabah} berhasil.")

#             print(f" Sisa kas di ATM {self.lokasi}: Rp{self.saldo_kas:,}")
#         else:
#             print(f" [ATM {self.id_atm}] Saldo kas mesin tidak mencukupi.")


# class Nasabah:
#     def __init__(self, nama, nomor_rekening):
#         self.nama = nama
#         self.nomor_rekening = nomor_rekening  
#         # Tidak ada self.atm = ...
#         # Nasabah tidak memiliki mesin ATM secara permanen.
        
#     def tarik_tunai(self, atm, jumlah):
#         """Asosiasi: MesinATM diterima sebagai parameter dan dipakai
#         sementara."""
#         print(f" {self.nama} memasukkan kartu ke ATM unit {atm.id_atm} ({atm.lokasi})...")
#         atm.proses_penarikan(self.nama, jumlah)


# # Kedua objek dibuat secara independen
# atm_pusat = MesinATM("ATM-01", "Kantor Cabang Sudirman", 50000000)
# budi = Nasabah("Budi Santoso", "101-220-334")
# siti = Nasabah("Siti Rahma", "101-445-889")

# # Asosiasi berjalan saat method dipanggil
# budi.tarik_tunai(atm_pusat, 500000)
# # Mesin ATM yang sama bisa digunakan oleh nasabah lain
# siti.tarik_tunai(atm_pusat, 1000000)

class Karyawan:
    def __init__(self, nama, nip, posisi):
        self.nama = nama
        self.nip = nip
        self.posisi = posisi

    @property
    def info_singkat(self):
        return f"{self.nama} ({self.posisi}) - NIP: {self.nip}"
    def __str__(self):
        return f"Karyawan: {self.nama} | NIP: {self.nip} | Posisi: {self.posisi}"

    
class Bank:
    def __init__(self, nama_bank, kode):
        self.nama_bank = nama_bank
        self.kode = kode
        self._karyawan = [] # Agregasi: menampung referensi objek Karyawan dari luar

    def tambah_karyawan(self, karyawan):
        """Karyawan dibuat di luar dan didaftarkan ke dalam bank."""
        if isinstance(karyawan, Karyawan):
            self._karyawan.append(karyawan)
            print(f" [+] {karyawan.nama} mulai bekerja di {self.nama_bank}")

    def keluarkan_karyawan(self, nip):
        """Melepas referensi karyawan tanpa memusnahkan objek karyawan aslinya."""
        awal = len(self._karyawan)
        self._karyawan = [k for k in self._karyawan if k.nip != nip]
        if len(self._karyawan) < awal:
            print(f" [-] Karyawan dengan NIP {nip} telah berhenti dari {self.nama_bank}")

    @property
    def total_karyawan(self):
        return len(self._karyawan)

    def tampilkan_daftar_karyawan(self):
        print(f"\n Daftar Pegawai {self.nama_bank} (Kode: {self.kode})")
        print(f" Total: {self.total_karyawan} orang")
        for k in self._karyawan:
            print(f" - {k.info_singkat}")


# Objek Karyawan dibuat secara mandiri
teller = Karyawan("Andi Wijaya", "EMP01", "Teller")
manager = Karyawan("Dewi Lestari", "EMP02", "Branch Manager")

# Objek Bank menampung karyawan
bank_mandiri = Bank("Bank Nasional Mandiri", "BNM")
bank_mandiri.tambah_karyawan(teller)
bank_mandiri.tambah_karyawan(manager)
bank_mandiri.tampilkan_daftar_karyawan()

# Bukti siklus hidup agregasi: Bank dibubarkan
del bank_mandiri

# Objek karyawan tetap utuh di memori dan dapat bekerja di tempat lain
print(f"\n Data karyawan setelah entitas bank dihapus:")
print(f" {teller}")
print(f" {manager}")