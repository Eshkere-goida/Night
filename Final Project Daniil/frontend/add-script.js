const fileInput = document.getElementById('image_file');
const previewImg = document.getElementById('preview-img');
const previewContainer = document.getElementById('preview-container');


if (previewContainer) {
    previewContainer.style.display = "none";
}

if (fileInput) {
    fileInput.addEventListener('change', () => {
        const file = fileInput.files[0];
        if (file) {
            const tempUrl = URL.createObjectURL(file);
            previewImg.src = tempUrl;
            previewContainer.style.display = "block";
        }
    });
}

const form = document.getElementById('add-item-form');

if (form) {
    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData();
        formData.append("name", document.getElementById('name').value);
        formData.append("storage_sector", document.getElementById('sector').value);
        formData.append("quantity", document.getElementById('quantity').value);
        formData.append("weight", document.getElementById('weight').value || 0);
        formData.append("price", document.getElementById('price').value); // ДОБАВЛЯЕМ PRICE
        formData.append("is_dangerous", document.getElementById('is_dangerous').checked);
        formData.append("image_file", fileInput.files[0]);

        // Проверяем, что все поля заполнены
        if (!formData.get('price')) {
            alert("❌ Введите цену товара!");
            return;
        }

        const response = await fetch("http://127.0.0.1:8000/items", {
            method: "POST",
            body: formData
        });

        if (response.status === 201) {
            alert("✅ Товар успешно добавлен!");
            window.location.href = "index.html";
        } else {
            const error = await response.json();
            alert("❌ Ошибка при загрузке: " + JSON.stringify(error.detail));
            console.log(error);
        }
    });
}