document.addEventListener("DOMContentLoaded",async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const itemId = urlParams.get('id');

    if(!itemId) {
        alert("Товар не выбран!");
        window.location.href = "index.html";
        return;
    }

    const API_URL = `http://127.0.0.1:8000/items/${itemId}`;

    try {
        const response = await fetch(API_URL);
        if(!response.ok) {
            throw new Error("Товар не найден на сервере");
        }

        const item = await response.json();

        document.getElementById('item-name').textContent = item.name;
        document.getElementById('item-sector').textContent = item.storage_sector;
        document.getElementById('item-quantity').textContent = item.quantity;
        document.getElementById('item-weight').textContent = item.weight;

        const imageElement = document.getElementById('item-image');
        if (item.image_url) {
            imageElement.src = `http://127.0.0.1:8000${item.image_url}`;
        } else {
            imageElement.src = `http://127.0.0.1:8000/static/img/default.jpg`;
        }
        if(item.is_dangerous) {
            document.getElementById('danger-badge').style.display = 'block';
        } 
        const deleteBtn = document.getElementById('delete-btn');
        deleteBtn.addEventListener('click',async () => {
            const confirmDelete = confirm(`Вы уверены, что хотите списать груз "${item.name}"?`)
            if (!confirmDelete) return;
            const deleteResponse = await fetch(`${API_URL}?confirm=true`,{
                method: "DELETE"
            });
            
            if (deleteResponse.ok) {
                
                alert("Груз успешно списан со склада!");
                window.location.href = "index.html";
            } else {
                const errorData  = await deleteResponse.json();
                alert("Ошибка при удалении: " + (errorData.detail || "Не удалось списать товар"));
            }
        });
    } catch (error) {
        console.error("Ошибка:",error);
        document.getElementById('item-name').textContent = "❌ Ошибка загрузки данных";
    }
});