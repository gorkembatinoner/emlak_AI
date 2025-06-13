# 🏡 Emlak Fiyat Tahmini (Random Forest & Flask)

Bu proje, Tekirdağ bölgesindeki konutlar için hem **emlak fiyat tahmini** hem de **deprem risk haritası** sunar. Uygulama Python, Flask ve scikit-learn kullanılarak geliştirilmiştir. Görsel arayüz için Material Dashboard Flask teması entegre edilmiştir.

## 🚀 Projenin Özellikleri

- 📊 Random Forest Regressor kullanılarak eğitimli model
- 🌍 Harita tabanlı Tekirdağ iline özel mahalle ve ilçe verileri
- 🔥 Isıtma tipi, metrekare, oda sayısı ve bulunduğu bölge gibi parametreleri dikkate alan fiyat tahmini
- 🧠 Hazır eğitilmiş model (`random_forest_model.pkl`)
- 🎨 Material Dashboard teması ile zengin arayüz
- 📊 `openpyxl`, `pandas` ile veri dosyası işlemleri

## 📁 Proje Yapısı

emlak_AI/
├── app.py # Ana Flask uygulaması
├── random_forest_model.pkl # Eğitilmiş model
├── konum_encoded_LOO.xlsx # Bölge verileri (encoding)
├── Bölge_loo_map.csv # Harita ve bölge risk verisi
├── templates/
│ ├── index.html # Ana sayfa
│ ├── deprem_risk.html # Deprem haritası sayfası
│ ├── base.html # Taban şablon
│ └── styles.html # Stil içerikleri
├── static/
│ ├── css/
│ ├── js/
│ └── logo.png
├── requirements.txt # Python bağımlılıkları
├── material-dashboard-flask-master/ # UI şablon klasörü
│ └── ... (tema dosyaları)


1. Python ortamı oluştur:

```bash
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)

http://127.0.0.1:5000 ---> Tarayıcıdan bu adresi ziyaret ediniz
```

2. Gerekli Paketleri kur 

```bash
pip install -r requirements.txt
```

3. Uygulamayı Başlat

```bash
python app.py
```

4. Tarayıcında Aç

http://127.0.0.1:5000



### 📌 Kullanım

1_İlçe - Mahalle seçin.

2_Oda sayısı seçin.

3_Salon sayısı seçin.

4_Metrekare değerini girin.

5_Bulunduğu katı girin

6_Bina yaşı değerini girin

7_Isıtma tipinin seçin

8_Tahmin Et butonuna tıklayın.

Model, bu verilerle tahmini fiyatı size sunacaktır.