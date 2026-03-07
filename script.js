const grid = document.getElementById("inventory-grid");
const btn = document.getElementById("load-data");
const statusSpan = document.querySelector("#status-label span");
const priceInput = document.getElementById("price-filter");
const addBtn = document.getElementById("add-btn");

addBtn.onclick = function() {
    const newItem = {
        name:document.getElementById("new-name").value,
        price:parseInt(document.getElementById("new-price").value),
        status: "В наличии"
    };
    fetch('http://127.0.0.1:8000/items', {
        method: "POST",
        headers: {
            'Content-Type':'application.json'
        },
        body: JSON.stringify(newItem)
    })
    .then(res => res.json())
    .then(result => {
        console.log("Ответ сервера:",result);
        alert("Товар добавлен!");
        document.getElementById("load-data").click();

    });
};

function renderItems(data) {
    grid.innerHTML = "";
    items.forEach(itme => {
        grid.innerHTML+= `
            <div class="product-card">
                <h3>${item.name}</h3>
                <p>Цена: ${item.price}</p>
                <button class="delete-btn" onclick="deleteItem(${item.id})">🗑️ Удалить</button>
            </div>
            
        `;

    });
    if (data.length=== 0) {
        grid.innerHTML="<h2 class='empty'>Ничего не найдено...</h2>";
        return;
    }
    data.forEach(item => {
        grid.innerHTML += `
            <div class="product-card">
                <h3>${item.name}</h3>
                <p>Цена: ${item.price} 💰</p>
            </div>
        `;
    });
}

priceInput.oninput = function() {
    const val = priceInput.value;
    fetch(`http://127.0.0.1:8000/items?max_price=${val}`)
        .then(res => res.json())
        .then(data => {

            renderItems(data);
        });
};

btn.onclick = function() {
    fetch('http://127.0.0.1:8000/items')
        .then(response => response.json())
        .then(data => {
            grid.innerHTML = "";
            data.forEach(item => {
                const cardHTML = `
                    <div class="icon">📦</div>
                        <h3>${item.name}</h3>
                        <p class="price">${item.price} Кредитов</p>
                        <span class="badge">${item.status}</span>
                    </div>
                `;
                grid.innerHTML +=cardHTML;
            });
            statusSpan.innerText = "Подключено";
            statusSpan.style.color = "#22c55e";

        })
        .catch (err => {
            statusSpan.innerText = "Ошибка сервера!";
            statusSpan.style.color = "red";
            console.error("Сервер спит?", err);
        });
};

function deleteItemId(id) {
    if (!confirm("Вы уверены, что хотите списать это оборудование?")) return

}








const grid = document.getElementById("inventory-grid");
const btn = document.getElementById("load-data");
const statusSpan = document.querySelector("#status-label span");
const priceInput = document.getElementById("price-filter");
const addBtn = document.getElementById("add-btn");

// Добавление нового товара
addBtn.onclick = function() {
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
            'Content-Type': 'application/json'  // Исправлено!
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
        btn.click(); // Обновляем список
    })
    .catch(err => {
        console.error("Ошибка при добавлении:", err);
        alert("Ошибка при добавлении товара!");
    });
};

// Фильтрация по цене
priceInput.oninput = function() {
    const val = priceInput.value;
    if (val) {
        fetch(`http://127.0.0.1:8000/items?max_price=${val}`)
            .then(res => res.json())
            .then(data => {
                renderItems(data);
            })
            .catch(err => console.error("Ошибка фильтрации:", err));
    } else {
        btn.click(); // Если поле пустое, показываем все товары
    }
};

// Загрузка всех товаров
btn.onclick = function() {
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

// Функция отрисовки товаров
function renderItems(data) {
    grid.innerHTML = "";
    
    if (data.length === 0) {
        grid.innerHTML = "<h2 class='empty'>Ничего не найдено...</h2>";
        return;
    }
    
    data.forEach(item => {
        grid.innerHTML += `
            <div class="product-card">
                <div class="icon">📦</div>
                <h3>${item.name}</h3>
                <p class="price">${item.price} Кредитов</p>
                <span class="badge">${item.status}</span>
                <button class="delete-btn" onclick="deleteItem(${item.id})">🗑️ Удалить</button>
            </div>
        `;
    });
}

// Функция удаления товара
function deleteItem(id) {
    if (!confirm("Вы уверены, что хотите списать это оборудование?")) return;
    
    fetch(`http://127.0.0.1:8000/items/${id}`, {
        method: "DELETE"
    })
    .then(res => res.json())
    .then(result => {
        console.log("Удалено:", result);
        btn.click(); // Обновляем список
    })
    .catch(err => console.error("Ошибка при удалении:", err));
}

// Автоматическая загрузка при открытии страницы
document.addEventListener('DOMContentLoaded', btn.click);
