// Deprem risk haritası için gerekli değişkenler
let depremRiskHaritasi;
let depremRiskLayer;

// Harita başlatma fonksiyonu
function initDepremRiskHaritasi() {
    // Haritayı oluştur
    depremRiskHaritasi = L.map('deprem-risk-haritasi').setView([41.0, 27.5], 9);

    // OpenStreetMap katmanını ekle
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(depremRiskHaritasi);

    // Deprem risk katmanını ekle
    depremRiskLayer = L.geoJSON(null, {
        style: function(feature) {
            return {
                fillColor: getRiskColor(feature.properties.risk),
                weight: 2,
                opacity: 1,
                color: 'white',
                fillOpacity: 0.7
            };
        },
        onEachFeature: function(feature, layer) {
            layer.bindPopup(`
                <strong>${feature.properties.name}</strong><br>
                Risk Seviyesi: ${feature.properties.risk}<br>
                Açıklama: ${feature.properties.description}
            `);
        }
    }).addTo(depremRiskHaritasi);

    // Risk seviyesine göre renk belirleme fonksiyonu
    function getRiskColor(risk) {
        switch(risk.toLowerCase()) {
            case 'yüksek':
                return '#ff0000';
            case 'orta':
                return '#ffa500';
            case 'düşük':
                return '#00ff00';
            default:
                return '#808080';
        }
    }

    // Örnek veri (gerçek verilerle değiştirilmeli)
    const ornekVeri = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "name": "Çerkezköy",
                    "risk": "Orta",
                    "description": "Orta riskli bölge"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [27.9994, 41.2857]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "name": "Çorlu",
                    "risk": "Yüksek",
                    "description": "Yüksek riskli bölge"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [27.8000, 41.1591]
                }
            }
        ]
    };

    // Örnek veriyi haritaya ekle
    depremRiskLayer.addData(ornekVeri);
}

// Sayfa yüklendiğinde haritayı başlat
document.addEventListener('DOMContentLoaded', initDepremRiskHaritasi); 