import csv
import os

class AreaParkir:
    nama_instansi = "Terminal Parking Center"
    kapasitas_maksimal = 100
    total_kendaraan_aktif = 0

    def __init__(self, lokasi, pendapatan=0):
        self.lokasi = lokasi
        self.pendapatan = pendapatan

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
    tarif_mobil = 5000
    tarif_motor = 2000
    prefix_tiket = "TKT"

    def __init__(self, jenis, plat_nomor):
        self.jenis = jenis
        self.plat_nomor = plat_nomor

    @property
    def plat_nomor(self):
        return self.__plat_nomor

    @plat_nomor.setter
    def plat_nomor(self, nilai):
        if not nilai or len(nilai.strip()) < 4:
            raise ValueError("Plat nomor tidak valid (kosong atau kurang dari 4 karakter)!")
        self.__plat_nomor = nilai.strip().upper()

    def info_kendaraan(self):
        print(f"Jenis Kendaraan : {self.jenis}")
        print(f"Plat Nomor      : {self.__plat_nomor}")

    @classmethod
    def dari_data_string(cls, string_data):
        jenis, plat_nomor = string_data.split(",")
        return cls(jenis.strip(), plat_nomor.strip())

    @staticmethod
    def validasi_jenis(jenis):
        return jenis.strip().lower() in ("mobil", "motor")


class KarcisParkir:
    denda_hilang = 50000
    format_tanggal = "DD-MM-YYYY"
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
        print(f"[{self.id_karcis}] {self.objek_kendaraan.jenis} - {self.objek_kendaraan.plat_nomor} | Status: {status}")

    @classmethod
    def update_denda(cls, nominal_baru):
        cls.denda_hilang = nominal_baru

    @staticmethod
    def buat_id_karcis(nomor_urut):
        return f"{KarcisParkir.kode_lokasi}-{nomor_urut:04d}"

    @staticmethod
    def simpan_transaksi(database_karcis):
        with open("transaksi_parkir.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["id_karcis", "jenis_kendaraan", "plat_nomor", "status_lunas"])
            for karcis in database_karcis.values():
                writer.writerow([karcis.id_karcis, karcis.objek_kendaraan.jenis, karcis.objek_kendaraan.plat_nomor, karcis.status_lunas])

    @staticmethod
    def muat_transaksi():
        database = {}
        nomor_urut = 1
        if os.path.exists("transaksi_parkir.csv"):
            with open("transaksi_parkir.csv", mode="r") as file:
                reader = csv.reader(file)
                next(reader, None)
                for row in reader:
                    if len(row) == 4:
                        id_karcis, jenis, plat, status = row
                        kendaraan = Kendaraan(jenis, plat)
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

    jalankan_demo = input("Jalankan demonstrasi program (y/n)? ").strip().lower()
    
    if jalankan_demo == 'y':
        print("\n=== PENGUJIAN PROGRAM (DEMONSTRASI OOP) ===")
        
        # 1. Uji Class AreaParkir
        print("\n--- 1. Uji Class AreaParkir ---")
        area1 = AreaParkir("Blok A Reguler")
        area2 = AreaParkir("Blok B VIP")
        
        area1.pendapatan = 150000 
        try:
            area2.pendapatan = -50000 
        except ValueError as e:
            print(f"[Validasi Setter Area] Error tertangkap: {e}")
            
        AreaParkir.ubah_kapasitas(200)
        print(f"Ketersediaan slot (150 dari 200)? {AreaParkir.cek_ketersediaan(150, AreaParkir.kapasitas_maksimal)}")
        area1.rekap_area()

        # 2. Uji Class Kendaraan
        print("\n--- 2. Uji Class Kendaraan ---")
        mobil1 = Kendaraan("Mobil", "KT 1234 XX")
        motor1 = Kendaraan.dari_data_string("Motor, B 9999 YZ") 
        
        mobil1.plat_nomor = "KT 5678 ZZ"
        try:
            motor1.plat_nomor = "AB" 
        except ValueError as e:
            print(f"[Validasi Setter Kendaraan] Error tertangkap: {e}")
            
        print(f"Apakah 'Sepeda' jenis valid? {Kendaraan.validasi_jenis('Sepeda')}")
        mobil1.info_kendaraan()
        motor1.info_kendaraan()

        # 3. Uji Class KarcisParkir
        print("\n--- 3. Uji Class KarcisParkir ---")
        karcis1 = KarcisParkir(KarcisParkir.buat_id_karcis(1), mobil1)
        karcis2 = KarcisParkir(KarcisParkir.buat_id_karcis(2), motor1)
        
        karcis1.status_lunas = True  
        try:
            karcis2.status_lunas = "Sudah Bayar" 
        except ValueError as e:
            print(f"[Validasi Setter Karcis] Error tertangkap: {e}")
            
        KarcisParkir.update_denda(100000)
        print(f"Denda karcis hilang diubah menjadi: Rp{KarcisParkir.denda_hilang:,}")
        karcis1.cetak_karcis()
        karcis2.cetak_karcis()
        
        print("\nDemonstrasi selesai.")
        input("Tekan Enter untuk melanjutkan ke sistem CRUD interaktif...")

    # main program
    while True:
        print("\n" + "=" * 45)
        print("   SISTEM MANAJEMEN PARKIR KENDARAAN (CRUD)")
        print("=" * 45)
        print("1. [Create] Daftarkan Kendaraan Masuk")
        print("2. [Read]   Tampilkan Semua Kendaraan")
        print("3. [Update] Perbarui Data Plat/Status")
        print("4. [Delete] Hapus/Keluarkan Kendaraan")
        print("5. Lihat Rekap Area Parkir")
        print("6. Keluar Program")
        print("=" * 45)

        pilihan = input("Pilih menu (1-6): ")

        if pilihan == "1":
            if not AreaParkir.cek_ketersediaan(AreaParkir.total_kendaraan_aktif, AreaParkir.kapasitas_maksimal):
                print("\n[!] Gagal: Area parkir sudah penuh.")
                continue

            print("\n--- Create: Pendaftaran Kendaraan ---")
            input_data = input("Masukkan data (Jenis, Plat) [contoh: Mobil, KT 1234 XX]: ")
            
            try:
                kendaraan_baru = Kendaraan.dari_data_string(input_data)
                
                if not Kendaraan.validasi_jenis(kendaraan_baru.jenis):
                    print("[!] Gagal: Jenis kendaraan hanya boleh 'Mobil' atau 'Motor'.")
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
                print(f"\n[!] Gagal: {e}")
            except Exception:
                print("\n[!] Gagal: Format salah. Pastikan menggunakan tanda koma (,).")

        elif pilihan == "2":
            print("\n--- Read: Daftar Kendaraan Terparkir ---")
            if not database_karcis:
                print("Tidak ada kendaraan yang sedang terparkir saat ini.")
            else:
                for karcis in database_karcis.values():
                    karcis.cetak_karcis()

        elif pilihan == "3":
            print("\n--- Update: Perbarui Data ---")
            id_input = input("Masukkan ID Karcis (contoh: SMD-0001): ").strip().upper()
            
            if id_input in database_karcis:
                karcis = database_karcis[id_input]
                karcis.cetak_karcis()
                print("\nBagian yang ingin diperbarui:")
                print("a. Plat Nomor")
                print("b. Status Lunas (Proses Pembayaran)")
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
                        jenis = karcis.objek_kendaraan.jenis.lower()
                        tarif = Kendaraan.tarif_mobil if jenis == "mobil" else Kendaraan.tarif_motor
                        konfirmasi = input(f"Total tagihan Rp{tarif:,}. Lunasi sekarang? (Y/N): ")
                        
                        if konfirmasi.upper() == 'Y':
                            try:
                                karcis.status_lunas = True
                                area.pendapatan = area.pendapatan + tarif
                                area.simpan_data_area()
                                KarcisParkir.simpan_transaksi(database_karcis)
                                print("\n[+] Berhasil: Status menjadi LUNAS dan pendapatan bertambah.")
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
                print(f"\n[+] Berhasil: Data kendaraan {id_input} telah dihapus dari sistem.")
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