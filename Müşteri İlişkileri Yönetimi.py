from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QListWidget
from PyQt5.QtWidgets import QComboBox, QDateTimeEdit
from datetime import datetime
import sqlite3

class Musteri:
    def __init__(self, ad, iletisim_bilgileri):
        self.ad = ad
        self.iletisim_bilgileri = iletisim_bilgileri
        self.satislar = []  # Müşterinin satışları listesi
        self.destek_talepleri = []  # Müşterinin destek talepleri listesi

    def satis_ekle(self, satis):
        self.satislar.append(satis)  # Yeni bir satışı müşterinin satışları listesine ekler

    def destek_talebi_oluştur(self, destek_talebi):
        self.destek_talepleri.append(destek_talebi)  # Yeni bir destek talebini müşterinin destek talepleri listesine ekler

class Satis:
    def __init__(self, satis_no, urunler):
        self.satis_no = satis_no  # Satış numarası
        self.urunler = urunler  # Satılan ürünler listesi

class Destek:
    def __init__(self, talep_no, detaylar):
        self.talep_no = talep_no  # Destek talep numarası
        self.detaylar = detaylar  # Destek talebinin detayları

class Arayuz(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Müşteri İlişkileri Yönetimi (CRM) Uygulaması")
        self.musteriler = []  # Müşteriler listesi
        self.initUI()

    def initUI(self):
        self.result_label = QLabel()  # Sonuçları göstermek için etiket
        self.result_label.setStyleSheet("color: green; font-weight: bold;")  # Etiketin stilini belirle

        musteri_ekle_groupbox = self.create_musteri_ekle_groupbox()  # Müşteri ekleme bileşenlerini içeren grup kutusu
        satis_ekle_groupbox = self.create_satis_ekle_groupbox()  # Satış ekleme bileşenlerini içeren grup kutusu
        destek_talebi_olustur_groupbox = self.create_destek_talebi_olustur_groupbox()  # Destek talebi oluşturma bileşenlerini içeren grup kutusu

        main_layout = QVBoxLayout()  # Ana dikey düzen
        main_layout.addWidget(musteri_ekle_groupbox)  # Müşteri ekleme bileşenlerini ana düzene ekle
        main_layout.addWidget(satis_ekle_groupbox)  # Satış ekleme bileşenlerini ana düzene ekle
        main_layout.addWidget(destek_talebi_olustur_groupbox)  # Destek talebi oluşturma bileşenlerini ana düzene ekle
        main_layout.addWidget(self.result_label)  # Sonuçları göstermek için etiketi ana düzene ekle

        self.setLayout(main_layout)  # Ana düzeni ayarla

        self.create_database()  # Veritabanını oluştur

        self.populate_musteri_listwidget()  # Müşteri listesini başlangıçta doldur

    def create_database(self):
        conn = sqlite3.connect('crm.db')  # Veritabanına bağlan
        c = conn.cursor()

        # Müşteri tablosunu oluştur
        c.execute('''CREATE TABLE IF NOT EXISTS musteri
                     (ad TEXT, iletisim TEXT)''')

        # Satış tablosunu oluştur
        c.execute('''CREATE TABLE IF NOT EXISTS satis
                     (musteri_ad TEXT, satis_no TEXT, PRIMARY KEY (musteri_ad, satis_no))''')

        # Destek tablosunu oluştur
        c.execute('''CREATE TABLE IF NOT EXISTS destek
                     (musteri_ad TEXT, talep_no TEXT, PRIMARY KEY (musteri_ad, talep_no))''')

        conn.commit()
        conn.close()

    def create_musteri_ekle_groupbox(self):
        # Müşteri ekleme bileşenlerini içeren grup kutusu oluştur
        groupbox = QWidget()
        layout = QVBoxLayout()  # Dikey düzen
        groupbox.setLayout(layout)

        ad_label = QLabel("Müşteri Adı:")  # Etiket: Müşteri Adı
        self.ad_entry = QLineEdit()  # Metin girişi: Müşteri Adı
        layout.addWidget(ad_label)  # Etiketi düzene ekle
        layout.addWidget(self.ad_entry)  # Metin girişini düzene ekle

        iletisim_label = QLabel("İletişim Bilgileri:")  # Etiket: İletişim Bilgileri
        self.iletisim_entry = QLineEdit()  # Metin girişi: İletişim Bilgileri
        layout.addWidget(iletisim_label)  # Etiketi düzene ekle
        layout.addWidget(self.iletisim_entry)  # Metin girişini düzene ekle

        musteri_ekle_button = QPushButton("Müşteri Ekle")  # Buton: Müşteri Ekle
        musteri_ekle_button.clicked.connect(self.musteri_ekle)  # Butona tıklandığında müşteri ekleme işlemini gerçekleştirecek işlevi bağla
        layout.addWidget(musteri_ekle_button)  # Butonu düzene ekle

        return groupbox

    def create_satis_ekle_groupbox(self):
        # Satış ekleme bileşenlerini içeren grup kutusu oluştur
        groupbox = QWidget()
        layout = QVBoxLayout()  # Dikey düzen
        groupbox.setLayout(layout)

        musteri_label = QLabel("Müşteri:")  # Etiket: Müşteri
        self.musteri_listwidget = QListWidget()  # Liste: Müşteri
        layout.addWidget(musteri_label)  # Etiketi düzene ekle
        layout.addWidget(self.musteri_listwidget)  # Listeyi düzene ekle

        satis_no_label = QLabel("Satış Numarası:")  # Etiket: Satış Numarası
        self.satis_no_entry = QLineEdit()  # Metin girişi: Satış Numarası
        layout.addWidget(satis_no_label)  # Etiketi düzene ekle
        layout.addWidget(self.satis_no_entry)  # Metin girişini düzene ekle

        satis_ekle_button = QPushButton("Satış Ekle")  # Buton: Satış Ekle
        satis_ekle_button.clicked.connect(self.satis_ekle)  # Butona tıklandığında satış ekleme işlemini gerçekleştirecek işlevi bağla
        layout.addWidget(satis_ekle_button)  # Butonu düzene ekle

        return groupbox

    def create_destek_talebi_olustur_groupbox(self):
        # Destek talebi oluşturma bileşenlerini içeren grup kutusu oluştur
        groupbox = QWidget()
        layout = QVBoxLayout()  # Dikey düzen
        groupbox.setLayout(layout)

        musteri_label = QLabel("Müşteri:")  # Etiket: Müşteri
        self.musteri_listwidget_destek = QListWidget()  # Liste: Müşteri
        layout.addWidget(musteri_label)  # Etiketi düzene ekle
        layout.addWidget(self.musteri_listwidget_destek)  # Listeyi düzene ekle

        talep_no_label = QLabel("Talep Numarası:")  # Etiket: Talep Numarası
        self.talep_no_entry = QLineEdit()  # Metin girişi: Talep Numarası
        layout.addWidget(talep_no_label)  # Etiketi düzene ekle
        layout.addWidget(self.talep_no_entry)  # Metin girişini düzene ekle

        destek_talebi_olustur_button = QPushButton("Destek Talebi Oluştur")  # Buton: Destek Talebi Oluştur
        destek_talebi_olustur_button.clicked.connect(self.destek_talebi_olustur)  # Butona tıklandığında destek talebi oluşturma işlemini gerçekleştirecek işlevi bağla
        layout.addWidget(destek_talebi_olustur_button)  # Butonu düzene ekle

        return groupbox

    def musteri_ekle(self):
        ad = self.ad_entry.text()  # Metin girişinden müşteri adını al
        iletisim = self.iletisim_entry.text()  # Metin girişinden iletişim bilgilerini al

        if ad.strip() == "" or iletisim.strip() == "":  # Eğer müşteri adı veya iletişim bilgisi boşsa
            self.result_label.setText("Lütfen müşteri adı ve iletişim bilgilerini girin.")  # Kullanıcıya uygun bir hata mesajı göster
            return

        conn = sqlite3.connect('crm.db')  # Veritabanına bağlan
        c = conn.cursor()
        c.execute("INSERT INTO musteri (ad, iletisim) VALUES (?, ?)", (ad, iletisim))
        conn.commit()
        conn.close()

        self.populate_musteri_listwidget()  # Müşteri listesini güncelle
        self.result_label.setText("Müşteri başarıyla eklendi.")  # Başarılı bir ekleme olduğunu kullanıcıya bildir

    def satis_ekle(self):
        selected_musteri_index = self.musteri_listwidget.currentRow()  # Seçilen müşterinin dizinini al
        satis_no = self.satis_no_entry.text()  # Metin girişinden satış numarasını al

        if selected_musteri_index == -1:  # Eğer bir müşteri seçilmediyse
            self.result_label.setText("Lütfen bir müşteri seçin.")  # Kullanıcıya uygun bir hata mesajı göster
            return

        musteri = self.musteri_listwidget.item(selected_musteri_index).text()  # Seçilen müşteriyi al
        satis = Satis(satis_no, [])  # Yeni bir Satış örneği oluştur

        conn = sqlite3.connect('crm.db')  # Veritabanına bağlan
        c = conn.cursor()
        c.execute("INSERT INTO satis (musteri_ad, satis_no) VALUES (?, ?)", (musteri, satis_no))
        conn.commit()
        conn.close()

        self.result_label.setText("Satış başarıyla eklendi.")  # Başarılı bir ekleme olduğunu kullanıcıya bildir

    def destek_talebi_olustur(self):
        selected_musteri_index = self.musteri_listwidget_destek.currentRow()  # Seçilen müşterinin dizinini al
        talep_no = self.talep_no_entry.text()  # Metin girişinden talep numarasını al

        if selected_musteri_index == -1:  # Eğer bir müşteri seçilmediyse
            self.result_label.setText("Lütfen bir müşteri seçin.")  # Kullanıcıya uygun bir hata mesajı göster
            return

        musteri = self.musteri_listwidget_destek.item(selected_musteri_index).text()  # Seçilen müşteriyi al
        destek_talebi = Destek(talep_no, "")  # Yeni bir Destek örneği oluştur

        conn = sqlite3.connect('crm.db')  # Veritabanına bağlan
        c = conn.cursor()
        c.execute("INSERT INTO destek (musteri_ad, talep_no) VALUES (?, ?)", (musteri, talep_no))
        conn.commit()
        conn.close()

        self.result_label.setText("Destek talebi başarıyla oluşturuldu.")  # Başarılı bir ekleme olduğunu kullanıcıya bildir

    def populate_musteri_listwidget(self):
        self.musteri_listwidget.clear()  # Müşteri listesini temizle
        self.musteri_listwidget_destek.clear()  # Müşteri listesini temizle

        conn = sqlite3.connect('crm.db')  # Veritabanına bağlan
        c = conn.cursor()

        c.execute("SELECT ad FROM musteri")
        musteri_data = c.fetchall()
        for musteri in musteri_data:  # Her müşteri için
            self.musteri_listwidget.addItem(musteri[0])  # Müşteri adını listeye ekle
            self.musteri_listwidget_destek.addItem(musteri[0])  # Müşteri adını listeye ekle

        conn.close()

if __name__ == '__main__':
    app = QApplication([])  # PyQt uygulamasını başlat
    ex = Arayuz()  # Arayüz örneğini oluştur
    ex.show()  # Arayüzü göster
    app.exec_()  # Uygulamayı çalıştır
