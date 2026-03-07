const grid = document.getElementById("inventory-grid");
const btn = document.getElementById("load-data");
const statusSpan = document.querySelector("#status-label span");
const priceInput = document.getElementById("price-filter");
const addBtn = document.getElementById("add-btn");

updateStats()


addBtn.onclick = function () {
    const nameInput = document.getElementById("new-name");
    const priceInput = document.getElementById("new-price");

    if (!nameInput.value || !priceInput.value) {
        alert("Заполните все поля!");
        return;
    }

    const newItem = {
        name: nameInput.value,
        price: parseInt(priceInput.value),
        status: "В наличии"
    };

    fetch('http://127.0.0.1:8000/items', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(newItem)
    })
        .then(res => {
            if (!res.ok) {
                throw new Error(`HTTP error! status: ${res.status}`);
            }
            return res.json();
        })
        .then(result => {
            console.log("Ответ сервера:", result);
            alert("Товар добавлен!");
            nameInput.value = "";
            priceInput.value = "";
            btn.click();
            updateStats()
        })
        .catch(err => {
            console.error("Ошибка при добавлении:", err);
            alert("Ошибка при добавлении товара!");
        });
};

btn.onclick = function () {
    fetch('http://127.0.0.1:8000/items')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            renderItems(data);
            statusSpan.innerText = "Подключено";
            statusSpan.style.color = "#22c55e";
        })
        .catch(err => {
            statusSpan.innerText = "Ошибка сервера!";
            statusSpan.style.color = "red";
            console.error("Сервер спит?", err);
        });
};


priceInput.oninput = function () {
    const val = priceInput.value;
    if (val) {
        fetch(`http://127.0.0.1:8000/items?max_price=${val}`)
            .then(res => res.json())
            .then(data => {
                renderItems(data);
            })
            .catch(err => console.error("Ошибка фильтрации:", err));
    } else {
        btn.click();
    }
};




function updateStats() {
    fetch('http://127.0.0.1:8000/stats')
        .then(res => res.json())
        .then(data => {
            document.getElementById("stat-count").innerText = data.count;
            document.getElementById("stat-sum").innerText = data.total_price;
        });
}


function renderItems(data) {
    grid.innerHTML = "";

    if (data.length === 0) {
        grid.innerHTML = "<h2 class='empty'>Ничего не найдено...</h2>";
        return;
    }

    data.forEach(item => {
        const cardClass = item.price > 300 ? "product-card expensive" : "product-card";
        grid.innerHTML += `
            <div class="${cardClass}">
                <div class="icon">${item.price > 300 ? "💎" : "📦"}</div>
                <h3>${item.name}</h3>
                <p class="price">${item.price} Кредитов</p>
                <span class="badge">${item.status}</span>
                <button class="delete-btn" onclick="deleteItem(${item.id})">🗑️ Удалить</button>
            </div>
        `;
    });
}


function deleteItem(id) {
    if (!confirm("Вы уверены, что хотите списать это оборудование?")) return;

    fetch(`http://127.0.0.1:8000/items/${id}`, {
        method: "DELETE"
    })
        .then(res => res.json())
        .then(result => {
            console.log("Удалено:", result);
            btn.click();
            updateStats()
        })
        .catch(err => console.error("Ошибка при удалении:", err));
}


document.addEventListener('DOMContentLoaded', btn.click);