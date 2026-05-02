


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
        <div class="card-image-wrapper">
            <img src="http://127.0.0.0.1:8000${item.image_url}" alt = "${item.name}" class="item-img">
        </div>
        <div class="card-info">
            <span class="sector-tag">Сектор ${item.storage_sector}</span>
            <h3 class="item-name">${item.name}</h3>
            <p class="item-quantity">Количество: <strong>${item.quantity} шт.</strong></p>
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