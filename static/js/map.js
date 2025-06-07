let map;
let marker;

// Sayfa yüklendiğinde verileri al
fetch('/api/data')
    .then(response => response.json())
    .then(data => {
        window.ilceKoordinatlari = data.ilceKoordinatlari;
        
        // İlk haritayı oluştur
        map = L.map('map').setView([41.1591, 27.8000], 10); // Tekirdağ merkez
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);

        // Seçilen konum bilgisini al
        const konumSelect = document.querySelector('select[name="konum"]');
        if (konumSelect) {
            const selectedKonum = konumSelect.value;
            if (selectedKonum) {
                // İlçe ve mahalle adlarını ayır
                const [ilce, mahalle] = selectedKonum.split(' - ');
                
                // Not: Mahalle bazlı koordinat bilgisi mevcut olmadığı için, harita ilçe merkezine odaklanmaktadır.
                // Bu nedenle mahalle değişkeni şu anda harita odaklama için kullanılmamaktadır.
                if (window.ilceKoordinatlari && window.ilceKoordinatlari[ilce]) {
                    const [lat, lng] = window.ilceKoordinatlari[ilce];
                    
                    // Haritayı güncelle
                    map.setView([lat, lng], 13);
                    
                    // Eski marker'ı kaldır
                    if (marker) {
                        map.removeLayer(marker);
                    }
                    
                    // Yeni marker ekle
                    marker = L.marker([lat, lng])
                        .addTo(map)
                        .bindPopup(`<b>Konum:</b> ${ilce}`)
                        .openPopup();
                }
            }
        }
    });

// Konum seçildiğinde haritayı güncelle
document.querySelector('select[name="konum"]').addEventListener('change', function() {
    const selectedKonum = this.value;
    if (selectedKonum) {
        // İlçe ve mahalle adlarını ayır
        const [ilce, mahalle] = selectedKonum.split(' - ');
        
        if (window.ilceKoordinatlari && window.ilceKoordinatlari[ilce]) {
            const [lat, lng] = window.ilceKoordinatlari[ilce];
            
            // Haritayı güncelle
            map.setView([lat, lng], 13);
            
            // Eski marker'ı kaldır
            if (marker) {
                map.removeLayer(marker);
            }
            
            // Yeni marker ekle
            marker = L.marker([lat, lng])
                .addTo(map)
                .bindPopup(`<b>Konum:</b> ${ilce}`)
                .openPopup();
        }
    }
}); 