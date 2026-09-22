# class RekeningBankTanpaEncapsulation:
#     def __init__(self, pemilik, saldo):
#         self.pemilik = pemilik
#         self.saldo = saldo

# rekening = RekeningBankTanpaEncapsulation("Budi", 100000)
# rekening.saldo = -500000 # tidak ada yang mencegah ini
# print(rekening.saldo) # -500000, data jadi tidak valid

## public attribute
# class Mahasiswa:
#     def __init__(self, nama, nim):
#         self.nama = nama # public
#         self.nim = nim # public

# mhs = Mahasiswa("Dap", "2409106050")
# print(mhs.nama) # bisa diakses langsung
# print(mhs.nim)

## protected attribute
# class Karyawan:
#     def __init__(self, nama, gaji):
#         self.nama = nama
#         self._gaji = gaji # protected, hanya "disarankan" diakses dari dalam

# class Manager(Karyawan):
#     def tampilkan_gaji(self):
#         # subclass tetap bisa mengakses atribut protected milik parent
#         print(f"Gaji {self.nama}: {self._gaji}")

# manager = Manager("Daffa", 12000000)
# manager.tampilkan_gaji()
# print(manager._gaji) # masih bisa diakses, tapi secara konvensi sebaiknya tidak

## private attribute
# class RekeningBank:
#     def __init__(self, pemilik, saldo):
#         self.pemilik = pemilik
#         self.__saldo = saldo # private
#     def tarik_saldo(self, jumlah):
#         if jumlah > self.__saldo:
#             print("Saldo tidak cukup.")
#         elif jumlah <= 0:
#             print("Jumlah penarikan tidak valid.")
#         else:
#             self.__saldo -= jumlah
#             print(f"Berhasil menarik {jumlah}. Sisa saldo: {self.__saldo}")
#     def cek_saldo(self):
#         print(f"Saldo saat ini: {self.__saldo}")

# rekening = RekeningBank("Budi", 100000)
# rekening.tarik_saldo(30000)
# rekening.cek_saldo()
# print(rekening.__saldo) # AttributeError, karena sudah di-name-mangling

# # akses "paksa" ke private tetap mungkin lewat name mangling, tapi ini
# # melanggar konvensi encapsulation dan sebaiknya TIDAK dilakukan:
# print(rekening._RekeningBank__saldo) # 70000, tapi ini praktik yang buruk

class RekeningBank:
    def __init__(self, pemilik, saldo):
        self.pemilik = pemilik
        self.__saldo = saldo

    @property
    def saldo(self):
        """Getter -- dipanggil seperti atribut biasa, tanpa tanda kurung."""
        return self.__saldo
    
    @saldo.setter
    def saldo(self, saldo_baru):
        """Setter -- dijalankan otomatis saat ada assignment ke rekening.saldo"""
        if saldo_baru < 0:
            raise ValueError("Saldo tidak boleh negatif.")
        self.__saldo = saldo_baru

rekening = RekeningBank("Budi", 100000)
print(rekening.saldo) # dipanggil seperti atribut, bukan method
rekening.saldo = 250000 # otomatis lewat setter dengan validasi
print(rekening.saldo)
# rekening.saldo = -1000 # akan raise ValueError