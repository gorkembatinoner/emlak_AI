// Mahalle listelerini güncelle
function updateMahalleler() {
    const ilceSelect = document.getElementById('ilce');
    const mahalleSelect = document.getElementById('mahalle');
    const selectedIlce = ilceSelect.options[ilceSelect.selectedIndex].text;

    // Mahalle listesini temizle
    mahalleSelect.innerHTML = '<option value="">Mahalle seçiniz</option>';

    // Seçilen ilçeye göre mahalleleri ekle
    if (selectedIlce && window.mahalleData && window.mahalleData[selectedIlce]) {
        window.mahalleData[selectedIlce].forEach(mahalle => {
            const option = document.createElement('option');
            option.value = mahalle.id;
            option.textContent = mahalle.name;
            mahalleSelect.appendChild(option);
        });
    }
}

// Sayfa yüklendiğinde
document.addEventListener('DOMContentLoaded', function() {
    // İlçe seçildiğinde mahalle listesini güncelle
    document.getElementById('ilce').addEventListener('change', updateMahalleler);
}); 