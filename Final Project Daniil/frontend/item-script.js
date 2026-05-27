document.addEventListener("DOMContentLoaded", async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const itemId = urlParams.get('id');

    if (!itemId) {
        alert("Товар не выбран!");
        window.location.href = "index.html";
        return;
    }

    const API_URL = `http://127.0.0.1:8000/items/${itemId}`;

    try {
        const response = await fetch(API_URL);
        if (!response.ok) {
            throw new Error("Товар не найден на сервере");
        }

        const item = await response.json();

        document.getElementById('item-name').textContent = item.name;
        document.getElementById('item-sector').textContent = item.storage_sector;
        document.getElementById('item-quantity').textContent = item.quantity;
        document.getElementById('item-weight').textContent = item.weight;

        // Отображаем лайки
        const likesCountSpan = document.getElementById('likes-count');
        if (likesCountSpan) {
            likesCountSpan.textContent = item.likes ?? 0;
        }

        const imageElement = document.getElementById('item-image');
        if (item.image) {
            imageElement.src = `http://127.0.0.1:8000${item.image}`;
        } else {
            imageElement.src = `http://127.0.0.1:8000/static/img/default.jpg`;
        }

        if (item.is_dangerous) {
            document.getElementById('danger-badge').style.display = 'block';
        }

        // Кнопка удаления — внутри DOMContentLoaded, где item определён
        const deleteBtn = document.getElementById('delete-btn');
        deleteBtn.addEventListener('click', async () => {
            const confirmDelete = confirm(`Вы уверены, что хотите списать груз "${item.name}"?`);
            if (!confirmDelete) return;
            const deleteResponse = await fetch(`${API_URL}?confirm=true`, {
                method: "DELETE"
            });

            if (deleteResponse.ok) {
                alert("Груз успешно списан со склада!");
                window.location.href = "index.html";
            } else {
                const errorData = await deleteResponse.json();
                alert("Ошибка при удалении: " + (errorData.detail || "Не удалось списать товар"));
            }
        });

        // Кнопка лайка — тоже внутри, где itemId доступен
        const likeBtn = document.getElementById('like-btn');
        likeBtn.addEventListener('click', async () => {
            try {
                const likeResponse = await fetch(`http://127.0.0.1:8000/items/${itemId}/like`, {
                    method: 'POST'
                });
                if (!likeResponse.ok) throw new Error('Ошибка лайка');
                const likeData = await likeResponse.json();
                if (likesCountSpan) {
                    likesCountSpan.textContent = likeData.likes;
                }
            } catch (err) {
                console.error('Ошибка при лайке:', err);
            }
        });

    } catch (error) {
        console.error("Ошибка:", error);
        document.getElementById('item-name').textContent = "❌ Ошибка загрузки данных";
    }
});
