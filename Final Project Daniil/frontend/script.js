let userId = localStorage.getItem('warehouse_user_id');

if(!userId ) {
    userId = 'user_' + Math.random().toString(36).slice(2,11);
    localStorage.setItem('warehouse_user_id',userId);

    console.log("Создан новый ID пользователя:",userId);
} else {
    console.log("Пользователь узнан. Ваш ID:",userId);
}

async function addToCart(itemId) {
    const API_URL = `http://127.0.0.1:8000/cart/add/${itemId}?user_id=${userId}`;
    try {
        const response = await fetch(API_URL,{
            method: 'POST'
        });
        if (response.ok) {
            const data = await response.json();
            alert("Товар добавлен в корзину!");
            console.log("Состояние вашей корзиный на сервере:",data.cart);
        } else {
            alert("Ошибка: не удалось добавить товар.");
        }
    } catch (error) {
        console.error("Ошибка сети:",error);
        alert("Нет связи с сервером");
    }
    
}

const savedTheme = localStorage.theme;

if (savedTheme == "dark") {
    document.body.classList.add("dark-theme");
}

const themeBtn = document.querySelector("#theme-toggle");

if (document.body.classList.contains("dark-theme")) {
    themeBtn.innerText = "☀️ Светлая тема";
}
themeBtn.addEventListener("click",() => {
    document.body.classList.toggle("dark-theme");

    if (document.body.classList.contains("dark-theme")) {
        localStorage.setItem("theme","dark");
        themeBtn.innerText = "☀️ Светлая тема";

    } else {
        localStorage.setItem("theme","light");
        themeBtn.innerText = "🌙 Тёмная тема";
    }
})


const container = document.getElementById('items-container');


function loadItemsFromServer() {
    const API_URL = "http://127.0.0.1:8000/items";
    const loader = document.getElementById('loader');

    loader.style.display = "block";

    fetch (API_URL)
        .then(response => {
            if (!response.ok) {
                throw new Error("Ошибка: Сервер не отвечает или адрес не найден");
    
            }
            return response.json();
        })
        .then(data => {
            loader.style.display = "none";
            renderCards(data);
        })
        .catch(error => {
            loader.style.display = "none";
            console.error("Проблема с API:",error);
            const container = document.getElementById('items-container')
            container.innerHTML = "<h3>Ошибка подключения к базе данных склада</h3>";

        });
}
function updateTime() {
    const clockElement = document.getElementById('live-clock');
    const now = new Date();
    const timeString = now.toLocaleTimeString();

    clockElement.innerText = timeString;
}

async function handleLike(itemId) {
    try {
        const response = await fetch(`/items/${itemId}/like`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Ошибка при отправке лайка');
        }
        
        const data = await response.json();
        
        const likesSpan = document.getElementById(`likes-${itemId}`);
        if (likesSpan) {
            
            likesSpan.style.transform = 'scale(1.3)';
            setTimeout(() => {
                likesSpan.style.transform = 'scale(1)';
            }, 200);
            
            likesSpan.textContent = data.likes;
        }
        
        console.log(`Товар ${itemId} получил лайк! Теперь: ${data.likes}`);
        
    } catch (error) {
        console.error('Ошибка при лайке:', error);
        alert('Не удалось поставить лайк. Попробуйте позже.');
        }
}

function renderCards(items) {
    container.innerHTML = "";
    if (items.length === 0) {
        container.innerHTML = "<p>На складе пока нет зарегистрированных объектов.</p>";
        return;
    }
    items.forEach(item => {
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
        <div class="card-badge"> Сектор ${item.storage_sector}</div>
        <h3 class="card-title"> ${item.name} </h3>
        <p class="card-description"> Вес: ${item.weight} кг</p>

        <div class="card-stats">
            <span>Кол-во: <b>${item.quantity}</b> </span>
        </div>
        <div class="card-footer" style="display: flex;gap: 5px; margin-top: 10px;">
            <button class="btn-more" onclick="window.location.href='item.html?id=${item.id}'">📄</button>

            <button class="btn-cart" onclick="addToCart(${item.id})" style="flex-grow:1;background-color: #28a745; color: white;border:none;border-radius:5px;cursor:pointer;"> 🛒 В корзину </button>
        </div>
    `;
    if (item.is_dangerous) {
        const title = card.querySelector('.card-title');
        title.style.color = "red";

    }
    container.appendChild(card)
    });
}

function loadStats() {
    fetch("http://127.0.0.1/items/count")
        .then(res => res.json())
        .then(data => {
            document.getElementById('total-count').innerText = data.total;
        })
        .catch(err => console.error("Ошибка при получении статистики:",err));
}

const searchInput = document.getElementById('search-input');
const searchBtn = document.getElementById('search-btn');

searchInput.addEventListener('input', () => {
    const query = searchInput.value;
    const url = query
        ? `http://127.0.0.1:8000/items/search?name=${query}`
        : "http://127.0.0.1:8000/items";
    
    fetch(url)
        .then(res => res.json())
        .then(data => renderCards(data))
    
});

searchBtn.addEventListener('click', () => {
    const query = searchInput.value;
    fetch(`http://127.0.0.1:8000/items/search?name=${query}`)
        .then(res => res.json())
        .then(filteredData => {
            renderCards(filteredData)
        })
})
const refreshBtn = document.getElementById('refresh-btn');

const dangerBtn = document.getElementById('danger-filter') 
dangerBtn.addEventListener("click", () => {
    fetch("http://127.0.0.1:8000/items")
        .then(res => res.json())
        .then(data => {
            const filtered = data.filter(item => item.is_dangerous === true);
            renderCards(filtered);
        });
});
refreshBtn.addEventListener('click', () => {
    loadItemsFromServer();
});

loadItemsFromServer();
loadStats();

setInterval(updateTime,1000)