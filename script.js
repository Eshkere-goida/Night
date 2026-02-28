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