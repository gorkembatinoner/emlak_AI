function updateMahalleler() {
    const ilceSelect = document.getElementById('ilce');
    const mahalleSelect = document.getElementById('mahalle');
    const ilceKey = ilceSelect.value;
    const ilceName = ilceData[ilceKey];
    mahalleSelect.innerHTML = '';
    if (ilceName && mahalleData[ilceName]) {
        mahalleData[ilceName].forEach(function(mahalle) {
            const option = document.createElement('option');
            option.value = mahalle.id;
            option.textContent = mahalle.name;
            mahalleSelect.appendChild(option);
        });
    } else {
        const option = document.createElement('option');
        option.value = '';
        option.textContent = 'Önce ilçe seçiniz';
        mahalleSelect.appendChild(option);
    }
} 