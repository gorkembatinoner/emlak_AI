from flask import Flask, render_template, request, url_for, jsonify
import pandas as pd
import numpy as np
import os
import joblib

app = Flask(__name__, static_folder='static')

# Modeli yükle
try:
    model = joblib.load('random_forest_model.pkl')
    print("Model başarıyla yüklendi")
except Exception as e:
    print(f"Model yüklenirken hata oluştu: {str(e)}")
    model = None

# CSV dosyasını oku
bolge_df = pd.read_csv('Bölge_loo_map.csv')

# Bölge seçeneklerini oluştur
bolge_options = {}
for _, row in bolge_df.iterrows():
    ilce_mahalle = row['Bölge']
    encoded = row['Bölge_encoded']
    bolge_options[ilce_mahalle] = encoded

# Isınma tipi mapping
isinma_mapping = {
    'isinma_kombi': 0,
    'isinma_merkezi': 1,
    'isinma_yerden ısıtma': 2,
    'isinma_diğer': 3
}

# Model için gerekli sütunları tanımla
X_columns = ['Oda', 'Salon', 'Net Metrekare', 'Bulunduğu Kat', 'Bina Yaşı', 'Bölge_encoded', 'Isınma_Tipi_Encoded']

# Seçenekler için sözlük
column_options = {
    "İlçe": {
        0: "Ergene - Marmaracık Mahallesi",
        1: "Kapaklı - Atatürk Mahallesi",
        2: "Kapaklı - Bahçelievler Mahallesi",
        3: "Kapaklı - Cumhuriyet Mahallesi",
        4: "Kapaklı - İnönü Mahallesi",
        5: "Kapaklı - İsmet Paşa Mahallesi",
        6: "Süleymanpaşa - 100. Yıl Mahallesi",
        7: "Süleymanpaşa - Altınova Mahallesi",
        8: "Süleymanpaşa - Atatürk Mahallesi",
        9: "Süleymanpaşa - Aydoğdu Mahallesi",
        10: "Süleymanpaşa - Cumhuriyet Mahallesi",
        11: "Süleymanpaşa - Ertuğrul Mahallesi",
        12: "Süleymanpaşa - Hürriyet Mahallesi",
        13: "Süleymanpaşa - Karadeniz Mahallesi",
        14: "Süleymanpaşa - Kumbağ Mahallesi",
        15: "Süleymanpaşa - Ortacami Mahallesi",
        16: "Süleymanpaşa - Yavuz Mahallesi",
        17: "Süleymanpaşa - Zafer Mahallesi",
        18: "Süleymanpaşa - Çiftlikönü Mahallesi",
        19: "Süleymanpaşa - Çınarlı Mahallesi",
        20: "Çerkezköy - Bağlık Mahallesi",
        21: "Çerkezköy - Cumhuriyet Mahallesi",
        22: "Çerkezköy - Fatih Mahallesi",
        23: "Çerkezköy - Fevzi Paşa Mahallesi",
        24: "Çerkezköy - Gazi Mustafa Kemalpaşa Mahallesi",
        25: "Çerkezköy - Gazi Osman Paşa Mahallesi",
        26: "Çerkezköy - Kızılpınar Atatürk Mahallesi",
        27: "Çerkezköy - Kızılpınar Gültepe Mahallesi",
        28: "Çerkezköy - Kızılpınar Namık Kemal Mahallesi",
        29: "Çerkezköy - Veliköy Mahallesi",
        30: "Çerkezköy - Yıldırım Beyazıt Mahallesi",
        31: "Çerkezköy - İstasyon Mahallesi",
        32: "Çorlu - Alipaşa Mahallesi",
        33: "Çorlu - Cemaliye Mahallesi",
        34: "Çorlu - Cumhuriyet Mahallesi",
        35: "Çorlu - Hatip Mahallesi",
        36: "Çorlu - Havuzlar Mahallesi",
        37: "Çorlu - Hürriyet Mahallesi",
        38: "Çorlu - Hıdırağa Mahallesi",
        39: "Çorlu - Kazımiye Mahallesi",
        40: "Çorlu - Kemalettin Mahallesi",
        41: "Çorlu - Muhittin Mahallesi",
        42: "Çorlu - Nusratiye Mahallesi",
        43: "Çorlu - Reşadiye Mahallesi",
        44: "Çorlu - Rumeli Mahallesi",
        45: "Çorlu - Zafer Mahallesi",
        46: "Çorlu - Çobançeşme Mahallesi",
        47: "Çorlu - Şeyh Sinan Mahallesi",
        48: "Şarköy - Cumhuriyet Mahallesi",
        49: "Şarköy - İstiklal Mahallesi"
    },
    "Isıtma": {
        0: "Kombi",
        1: "Merkezi",
        2: "Yerden Isıtma",
        3: "Diğer"
    }
}

def tahmin_yap():
    try:
        data = request.get_json()
        
        oda = int(data['oda'])
        metrekare = float(data['metrekare'])
        bina_yasi = int(data['bina_yasi'])
        bolge = data['bolge']  # Artık ilçe-mahalle formatında
        isinma_tipi = int(data['isinma_tipi'])  # Doğrudan integer'a çevir

        # Bölge kodunu al
        bolge_encoded = bolge_options.get(bolge)
        if bolge_encoded is None:
            return jsonify({'error': 'Geçersiz bölge seçimi'}), 400

        # Özellikleri numpy array olarak hazırla
        X_new = np.array([[metrekare, oda, metrekare, bina_yasi, metrekare, isinma_tipi, bolge_encoded]])

        # Tahmin yap
        tahmin = model.predict(X_new)

        return jsonify({
            'tahmin': float(tahmin[0]),
            'formatli_tahmin': f"{tahmin[0]:,.2f} TL"
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
# Ana sayfa
@app.route('/', methods=['GET', 'POST'])
def index():
    print("Route çağrıldı, method:", request.method)  # Debug için
    
    # İlçe-mahalle gruplandırmasını oluştur
    ilce_mahalle_gruplari = {}
    for ilce_mahalle in column_options['İlçe'].values():
        ilce = ilce_mahalle.split(' - ')[0]
        if ilce not in ilce_mahalle_gruplari:
            ilce_mahalle_gruplari[ilce] = []
        ilce_mahalle_gruplari[ilce].append(ilce_mahalle)
    
    if request.method == 'POST':
        print("POST isteği alındı")  # Debug için
        try:
            print("Form verileri:", request.form)  # Form verilerini yazdır
            input_data = {}
            selected_options = {}
            
            # Konum bilgisini al
            konum = request.form.get('konum')
            print("Seçilen konum:", konum)  # Seçilen konumu yazdır
            if konum:
                selected_options['İlçe'] = konum
                # Bölge kodunu al
                bolge_encoded = bolge_options.get(konum)
                if bolge_encoded is not None:
                    input_data['İlçe'] = bolge_encoded
                else:
                    raise ValueError("Geçersiz bölge seçimi")
            
            # Oda sayısı, salon sayısı, metrekare, bulunduğu kat ve bina yaşını al
            oda_sayisi = request.form.get('oda_sayisi')
            if oda_sayisi:
                input_data['Oda Sayısı'] = int(oda_sayisi)
                selected_options['Oda Sayısı'] = oda_sayisi
            
            salon_sayisi = request.form.get('salon_sayisi')
            if salon_sayisi:
                input_data['Salon Sayısı'] = int(salon_sayisi)
                selected_options['Salon Sayısı'] = salon_sayisi
            
            metrekare = request.form.get('metrekare')
            if metrekare:
                input_data['Metrekare'] = float(metrekare)
                selected_options['Metrekare'] = metrekare
            
            bulundugu_kat = request.form.get('bulundugu_kat')
            if bulundugu_kat:
                input_data['Bulunduğu Kat'] = int(bulundugu_kat)
                selected_options['Bulunduğu Kat'] = bulundugu_kat
            
            bina_yasi = request.form.get('bina_yasi')
            if bina_yasi:
                input_data['Bina Yaşı'] = int(bina_yasi)
                selected_options['Bina Yaşı'] = bina_yasi
            
            # Isıtma tipini al
            isitma = request.form.get('isitma')
            if isitma:
                isitma_value = int(isitma)
                input_data['Isıtma'] = isitma_value
                selected_options['Isıtma'] = column_options['Isıtma'][isitma_value]

            print("İşlenmiş veriler:", input_data)  # İşlenmiş verileri yazdır

            # Eksik sütunları 0 ile doldur
            for col in X_columns:
                if col not in input_data:
                    input_data[col] = 0

            # DataFrame oluştur ve tahmin yap
            input_df = pd.DataFrame([{
                'Oda': input_data.get('Oda Sayısı', 0),
                'Salon': input_data.get('Salon Sayısı', 0),
                'Net Metrekare': input_data.get('Metrekare', 0),
                'Bulunduğu Kat': input_data.get('Bulunduğu Kat', 0),
                'Bina Yaşı': input_data.get('Bina Yaşı', 0),
                'Bölge_encoded': input_data.get('İlçe', 0),
                'Isınma_Tipi_Encoded': isinma_mapping.get(f"isinma_{input_data.get('Isıtma', 'kombi')}", 0)
            }])
            input_df = input_df[X_columns]
            
            print("DataFrame:", input_df)  # DataFrame'i yazdır
            
            if model is None:
                raise ValueError("Model yüklenemedi")
            
            # Tahmin yap
            predicted_price = model.predict(input_df)
            print("Tahmin sonucu:", predicted_price)  # Tahmin sonucunu yazdır
            
            # Sonucu formatla
            formatted_price = "{:,.2f}".format(predicted_price[0])
            print("Formatlanmış fiyat:", formatted_price)  # Formatlanmış fiyatı yazdır
            
            return render_template('index.html', 
                                 predicted_price=formatted_price, 
                                 column_options=column_options,
                                 selected_options=selected_options,
                                 ilce_mahalle_gruplari=ilce_mahalle_gruplari)
        except Exception as e:
            print(f"Hata oluştu: {str(e)}")  # Hata mesajını yazdır
            return render_template('index.html', 
                                 predicted_price=None, 
                                 column_options=column_options,
                                 selected_options=None,
                                 ilce_mahalle_gruplari=ilce_mahalle_gruplari,
                                 error=f"Tahmin yapılırken bir hata oluştu: {str(e)}")

    return render_template('index.html', 
                         predicted_price=None, 
                         column_options=column_options,
                         selected_options=None,
                         ilce_mahalle_gruplari=ilce_mahalle_gruplari)

@app.route('/api/data')
def get_data():
    return jsonify({
        'ilce': column_options['İlçe'],
        'ilceKoordinatlari': {
            "Çerkezköy": [41.2857, 27.9994],
            "Çorlu": [41.1591, 27.8000],
            "Ergene": [41.1667, 27.8667],
            "Hayrabolu": [41.3667, 27.1000],
            "Kapaklı": [41.3333, 27.9833],
            "Malkara": [40.8833, 26.9000],
            "Marmaraereğlisi": [40.9667, 27.9500],
            "Muratlı": [41.1667, 27.5000],
            "Saray": [41.4500, 27.9167],
            "Süleymanpaşa": [40.9833, 27.5167],
            "Şarköy": [40.6167, 27.1167]
        }
    })

@app.route('/deprem_risk')
def deprem_risk():
    return render_template('deprem_risk.html')

if __name__ == '__main__':
    app.run(debug=True) 