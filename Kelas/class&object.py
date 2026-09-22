class Product:
    def __init__(self, name, price, stock, category, brand):
        self.name = name
        self.price = price
        self.stock = stock
        self.category = category
        self.brand = brand
    
    def tambah_stok(self, jumlah):
        self.stock += jumlah

    def kurangi_stok(self, jumlah):
        if self.stock >= jumlah:
            self.stock -= jumlah

    def ubah_harga(self, harga_baru):
        self.price = harga_baru


class Laptop:
    def __init__(self, brand, price,):
        self.brand = brand
        self.price = price

    def show_info(self):
        print(f"brand: {self.brand}, price: {self.price}")

    def change_price(self, new_price):
        self.price = new_price

laptop1 = Laptop("Lenovo", 8000000)
laptop2 = Laptop("Asus", 10000000)
laptop3 = Laptop("HP", 12000000)

laptop1.change_price(10000000)
laptop2.change_price(20000000)

laptop1.show_info()
laptop2.show_info()
laptop3.show_info()