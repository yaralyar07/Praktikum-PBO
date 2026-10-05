import csv
import os
import random

class Loket:
    def __init__(self, nama_loket):
        self.nama_loket = nama_loket

    def info_loket(self):
        return f"Loket Aktif: {self.nama_loket}"


class Petugas:
    def __init__(self, nama_petugas):
        self.nama_petugas = nama_petugas

    def proses_pembayaran(self, karcis, tarif, area):
        print(f"Petugas '{self.nama_petugas}' memproses pembayaran Karcis {karcis.id_karcis} sebesar Rp{tarif:,}")
        karcis.status_lunas = True
        area.pendapatan = area.pendapatan + tarif


class AreaParkir:
    nama_instansi = "Terminal Parking Center"
    kapasitas_maksimal = 100
    total_kendaraan_aktif = 0

    def __init__(self, lokasi, pendapatan=0):
        self.lokasi = lokasi
        self.pendapatan = pendapatan
        self.loket_utama = Loket(f"Loket Utama {lokasi}")

    @property
    def pendapatan(self):
        return self.__pendapatan

    @pendapatan.setter
    def pendapatan(self, nilai):
        if nilai < 0:
            raise ValueError("Pendapatan tidak boleh bernilai negatif!")
        self.__pendapatan = nilai

    def rekap_area(self):
        print("=" * 45)
        print(f"REKAP AREA PARKIR - {AreaParkir.nama_instansi}")
        print("=" * 45)
        print(f"Lokasi           : {self.lokasi}")
        print(f"Fasilitas        : {self.loket_utama.info_loket()}")
        print(f"Kendaraan Aktif  : {AreaParkir.total_kendaraan_aktif}/{AreaParkir.kapasitas_maksimal}")
        print(f"Total Pendapatan : Rp{int(self.__pendapatan):,}")
        print("=" * 45)

    @classmethod
    def ubah_kapasitas(cls, kapasitas_baru):
        cls.kapasitas_maksimal = kapasitas_baru

    @staticmethod
    def cek_ketersediaan(jumlah_saat_ini, kapasitas):
        return jumlah_saat_ini < kapasitas

    def simpan_data_area(self):
        with open("status_area.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["lokasi", "kapasitas_maksimal", "total_kendaraan_aktif", "total_pendapatan"])
            writer.writerow([self.lokasi, AreaParkir.kapasitas_maksimal, AreaParkir.total_kendaraan_aktif, self.pendapatan])

    @classmethod
    def muat_data_area(cls):
        if os.path.exists("status_area.csv"):
            with open("status_area.csv", mode="r") as file:
                reader = csv.reader(file)
                next(reader, None)
                row = next(reader, None)
                if row:
                    lokasi = row[0]
                    cls.kapasitas_maksimal = int(row[1])
                    cls.total_kendaraan_aktif = int(row[2])
                    area = cls(lokasi)
                    area.pendapatan = float(row[3])
                    return area
        return cls("Jl. Sudirman No. 10, Samarinda")


class Kendaraan:
    def __init__(self, plat_nomor):
        self._plat_nomor = plat_nomor
        self.__id_mesin = f"SYS-{random.randint(1000, 9999)}"

    @property
    def plat_nomor(self):
        return self._plat_nomor

    @plat_nomor.setter
    def plat_nomor(self, nilai):
        if not nilai or len(nilai.strip()) < 4:
            raise ValueError("Plat nomor tidak valid (kosong atau kurang dari 4 karakter)!")
        self._plat_nomor = nilai.strip().upper()

    def info_kendaraan(self):
        print(f"ID Mesin Sistem : {self.__id_mesin}")
        print(f"Plat Nomor      : {self._plat_nomor}")


# SUBCLASS 1
class Mobil(Kendaraan):
    tarif_parkir = 5000

    def __init__(self, plat_nomor, jumlah_pintu):
        super().__init__(plat_nomor)
        self.jumlah_pintu = jumlah_pintu

    def info_kendaraan(self):
        print("--- Info Mobil ---")
        super().info_kendaraan()
        print(f"Jenis Kendaraan : Mobil")
        print(f"Jumlah Pintu    : {self.jumlah_pintu}")


class Motor(Kendaraan):
    tarif_parkir = 2000

    def __init__(self, plat_nomor, kapasitas_mesin):
        super().__init__(plat_nomor)
        self.kapasitas_mesin = kapasitas_mesin

    def info_kendaraan(self):
        print("--- Info Motor ---")
        super().info_kendaraan()
        print(f"Jenis Kendaraan : Motor")
        print(f"Kapasitas Mesin : {self.kapasitas_mesin} CC")


class KarcisParkir:
    denda_hilang = 50000
    kode_lokasi = "SMD"

    def __init__(self, id_karcis, objek_kendaraan, status_lunas=False):
        self.id_karcis = id_karcis
        self.objek_kendaraan = objek_kendaraan
        self.status_lunas = status_lunas

    @property
    def status_lunas(self):
        return self.__status_lunas

    @status_lunas.setter
    def status_lunas(self, nilai):
        if not isinstance(nilai, bool):
            raise ValueError("Status lunas harus bertipe boolean (True/False)!")
        self.__status_lunas = nilai

    def cetak_karcis(self):
        status = "LUNAS" if self.__status_lunas else "BELUM LUNAS"
        jenis = "Mobil" if isinstance(self.objek_kendaraan, Mobil) else "Motor"
        print(f"[{self.id_karcis}] {jenis} - {self.objek_kendaraan.plat_nomor} | Status: {status}")

    @staticmethod
    def buat_id_karcis(nomor_urut):
        return f"{KarcisParkir.kode_lokasi}-{nomor_urut:04d}"

    @staticmethod
    def simpan_transaksi(database_karcis):
        with open("transaksi_parkir.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["id_karcis", "jenis_kendaraan", "plat_nomor", "info_tambahan", "status_lunas"])
            for karcis in database_karcis.values():
                kendaraan = karcis.objek_kendaraan
                if isinstance(kendaraan, Mobil):
                    writer.writerow([karcis.id_karcis, "Mobil", kendaraan.plat_nomor, kendaraan.jumlah_pintu, karcis.status_lunas])
                elif isinstance(kendaraan, Motor):
                    writer.writerow([karcis.id_karcis, "Motor", kendaraan.plat_nomor, kendaraan.kapasitas_mesin, karcis.status_lunas])

    @staticmethod
    def muat_transaksi():
        database = {}
        nomor_urut = 1
        if os.path.exists("transaksi_parkir.csv"):
            with open("transaksi_parkir.csv", mode="r") as file:
                reader = csv.reader(file)
                next(reader, None)
                for row in reader:
                    if len(row) == 5:
                        id_karcis, jenis, plat, info, status = row
                        if jenis == "Mobil":
                            kendaraan = Mobil(plat, int(info))
                        else:
                            kendaraan = Motor(plat, int(info))
                            
                        karcis = KarcisParkir(id_karcis, kendaraan)
                        karcis.status_lunas = (status == "True")
                        database[id_karcis] = karcis
                        urut = int(id_karcis.split("-")[1])
                        if urut >= nomor_urut:
                            nomor_urut = urut + 1
        return database, nomor_urut


if __name__ == "__main__":
    area = AreaParkir.muat_data_area()
    database_karcis, nomor_urut = KarcisParkir.muat_transaksi()
    
    # Asosiasi: Inisialisasi petugas jaga hari ini
    petugas_jaga = Petugas("Budi")

    while True:
        print("\n" + "=" * 45)
        print("   SISTEM MANAJEMEN PARKIR KENDARAAN   ")
        print("=" * 45)
        print("1. Daftarkan Kendaraan Masuk")
        print("2. Tampilkan Semua Kendaraan")
        print("3. Perbarui Data / Bayar Parkir")
        print("4. Keluarkan Kendaraan")
        print("5. Lihat Rekap Area Parkir")
        print("6. Keluar Program")
        print("=" * 45)

        pilihan = input("Pilih menu (1-6): ")

        if pilihan == "1":
            if not AreaParkir.cek_ketersediaan(AreaParkir.total_kendaraan_aktif, AreaParkir.kapasitas_maksimal):
                print("\n[!] Gagal: Area parkir sudah penuh.")
                continue

            print("\n--- Create: Pendaftaran Kendaraan ---")
            jenis = input("Jenis Kendaraan (1. Mobil / 2. Motor): ").strip()
            plat = input("Masukkan Plat Nomor: ").strip()

            try:
                if jenis == "1":
                    pintu = int(input("Masukkan jumlah pintu mobil: "))
                    kendaraan_baru = Mobil(plat, pintu)
                elif jenis == "2":
                    cc = int(input("Masukkan kapasitas mesin (CC) motor: "))
                    kendaraan_baru = Motor(plat, cc)
                else:
                    print("[!] Pilihan jenis kendaraan tidak valid.")
                    continue

                id_baru = KarcisParkir.buat_id_karcis(nomor_urut)
                karcis_baru = KarcisParkir(id_baru, kendaraan_baru)
                
                database_karcis[id_baru] = karcis_baru
                AreaParkir.total_kendaraan_aktif += 1
                nomor_urut += 1

                area.simpan_data_area()
                KarcisParkir.simpan_transaksi(database_karcis)

                print(f"\n[+] Berhasil: Kendaraan masuk dengan ID {id_baru}.")
            except ValueError as e:
                print(f"\n[!] Gagal: {e} atau Inputan angka tidak valid.")

        elif pilihan == "2":
            print("\n--- Read: Daftar Kendaraan Terparkir ---")
            if not database_karcis:
                print("Tidak ada kendaraan yang sedang terparkir saat ini.")
            else:
                for karcis in database_karcis.values():
                    karcis.cetak_karcis()
                    print("  -> Detail:", end=" ")
                    karcis.objek_kendaraan.info_kendaraan()
                    print("-" * 30)

        elif pilihan == "3":
            print("\n--- Update: Perbarui Data ---")
            id_input = input("Masukkan ID Karcis (contoh: SMD-0001): ").strip().upper()
            
            if id_input in database_karcis:
                karcis = database_karcis[id_input]
                karcis.cetak_karcis()
                print("\nBagian yang ingin diperbarui:")
                print("a. Ubah Plat Nomor")
                print("b. Proses Pembayaran Parkir")
                opsi_update = input("Pilih opsi (a/b): ").strip().lower()
                
                if opsi_update == 'a':
                    plat_baru = input("Masukkan Plat Nomor baru: ")
                    try:
                        karcis.objek_kendaraan.plat_nomor = plat_baru
                        KarcisParkir.simpan_transaksi(database_karcis)
                        print("\n[+] Berhasil: Plat nomor telah diperbarui.")
                    except ValueError as e:
                        print(f"\n[!] Gagal update plat: {e}")
                
                elif opsi_update == 'b':
                    if karcis.status_lunas:
                        print("\n[!] Karcis ini sudah berstatus LUNAS.")
                    else:
                        tarif = karcis.objek_kendaraan.tarif_parkir
                        konfirmasi = input(f"Total tagihan Rp{tarif:,}. Lunasi sekarang? (Y/N): ")
                        
                        if konfirmasi.upper() == 'Y':
                            try:
                                petugas_jaga.proses_pembayaran(karcis, tarif, area)
                                
                                area.simpan_data_area()
                                KarcisParkir.simpan_transaksi(database_karcis)
                                print("\n[+] Berhasil: Pembayaran berhasil dicatat.")
                            except ValueError as e:
                                print(f"\n[!] Gagal: {e}")
                else:
                    print("\n[!] Opsi tidak valid.")
            else:
                print("\n[!] Data ID Karcis tidak ditemukan.")

        elif pilihan == "4":
            print("\n--- Delete: Keluarkan Kendaraan ---")
            id_input = input("Masukkan ID Karcis yang akan dihapus: ").strip().upper()
            
            if id_input in database_karcis:
                karcis = database_karcis[id_input]
                if not karcis.status_lunas:
                    print("\n[!] Peringatan: Karcis ini belum lunas. Hapus paksa?")
                    konfirmasi = input("Y/N: ")
                    if konfirmasi.upper() != 'Y':
                        print("Penghapusan dibatalkan.")
                        continue
                
                del database_karcis[id_input]
                AreaParkir.total_kendaraan_aktif -= 1
                
                area.simpan_data_area()
                KarcisParkir.simpan_transaksi(database_karcis)
                print(f"\n[+] Berhasil: Kendaraan {id_input} telah keluar dari area parkir.")
            else:
                print("\n[!] Data ID Karcis tidak ditemukan.")

        elif pilihan == "5":
            print("\n")
            area.rekap_area()

        elif pilihan == "6":
            print("\nSistem dimatikan. Terima kasih telah menggunakan layanan Terminal Parking Center.")
            break

        else:
            print("\n[!] Masukan tidak valid, silakan pilih angka 1 hingga 6.")