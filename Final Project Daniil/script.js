const fileInput = document.getElementById('image_file');
const previewImg = document.getElementById('preview-img');
const previewContainer = document.getElementById('preview-container');

// Превью изображения
previewContainer.style.display = "none";

fileInput.addEventListener('change', () => {
    const file = fileInput.files[0];
    if (file) {
        const tempUrl = URL.createObjectURL(file);
        previewImg.src = tempUrl;
        previewContainer.style.display = "block";
    }
});

// Отправка формы
const form = document.getElementById('add-item-form');

form.addEventListener('submit', async (event) => {
    event.preventDefault();
    
    // Получаем значения
    const name = document.getElementById('name').value;
    const sector = document.getElementById('sector').value;
    const quantity = document.getElementById('quantity').value;
    const weight = document.getElementById('weight').value || '0';
    const price = document.getElementById('price').value;  // ДОБАВЛЕНО
    const is_dangerous = document.getElementById('is_dangerous').checked;
    const imageFile = fileInput.files[0];
    
    // Проверяем обязательные поля
    if (!name) {
        alert("❌ Введите название товара!");
        return;
    }
    if (!sector) {
        alert("❌ Введите сектор!");
        return;
    }
    if (!quantity) {
        alert("❌ Введите количество!");
        return;
    }
    if (!price || price <= 0) {  // ПРОВЕРКА ЦЕНЫ
        alert("❌ Введите корректную цену!");
        return;
    }
    if (!imageFile) {
        alert("❌ Выберите изображение!");
        return;
    }
    
    // Создаем FormData
    const formData = new FormData();
    formData.append('name', name);
    formData.append('storage_sector', sector);
    formData.append('quantity', quantity);
    formData.append('weight', weight);
    formData.append('price', price);  // КЛЮЧЕВОЕ - ДОБАВЛЯЕМ PRICE В FORM DATA
    formData.append('is_dangerous', is_dangerous);
    formData.append('image_file', imageFile);
    
    // Отладка - смотрим что отправляем
    console.log("=== ОТПРАВЛЯЕМЫЕ ДАННЫЕ ===");
    for (let [key, value] of formData.entries()) {
        console.log(`${key}: ${value}`);
    }
    
    try {
        const response = await fetch('http://127.0.0.1:8000/items', {
            method: 'POST',
            body: formData
        });
        
        console.log("Статус ответа:", response.status);
        
        if (response.ok) {
            const data = await response.json();
            console.log("Успех:", data);
            alert('✅ Товар успешно добавлен!');
            window.location.href = 'index.html';
        } else {
            const error = await response.json();
            console.error("Ошибка сервера:", error);
            alert(`❌ Ошибка: ${JSON.stringify(error.detail || error)}`);
        }
    } catch (error) {
        console.error("Ошибка сети:", error);
        alert('❌ Ошибка подключения к серверу. Убедитесь, что сервер запущен.');
    }
});