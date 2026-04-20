const fileInput = document.getElementById('image_file');
const previewImg = document.getElementById('preview-img');
const previewContainer = document.getElementById('preview-container')

fileInput.addEventListener('change',()=> {
    const file = fileInput.files[0];
    if (file) {
        const tempUrl = URL.createObjectURL(file);
        previewImg.src = tempUrl;
        previewContainer.style.display = "block";
    }
    
});

const form = document.getElementById('add-item-form');

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const formData = new FormData();
    formData.append("name", document.getElementById('name').value);
    formData.append("storage_sector",document.getElementById('sector').value);
    formData.append("quantity", document.getElementById('quantity').value);
    formData.append("image_file",fileInput.files[0]);

    const response = await fetch("http://127.0.0.1:8000/items", {
        method: "POST",
        body: formData
    });

    if (response.status === 201) {
        alert("✅ Товар успешно добавлен!");
        window.location.href = "index.html";
    } else {
        alert("❌ Ошибка при загрузке. Проверь консоль браузера");
        console.log(await response.json());
    }
})