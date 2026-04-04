
items = [
    {
        "id" : 1,
        "name" : "Электро-Самокат",
        "storage_sector": 12,
        "weight" : 40,
        "quantity": 3,
        "price" : 300,
        "is_dangerous" : false
    },
    {
        "id" : 2,
        "name" : "Набор носков",
        "storage_sector":5,
        "weight" : 5,
        "quantity": 3,
        "price" : 40,
        "is_dangerous" : false
    },
    {
        "id" : 3,
        "name" : "Урановый стержень",
        "storage_sector":8,
        "weight" : 80,
        "quantity": 1,
        "price" : 800,
        "is_dangerous" : true
    },
    {
        "id" : 4,
        "name" : "Фосфорная кислота",
        "storage_sector":10,
        "weight" : 1,
        "quantity": 6,
        "price" : 450,
        "is_dangerous" : true
    }
]



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

function updateTime() {
    const clockElement = document.getElementById('live-clock');
    const now = new Date();
    const timeString = now.toLocaleTimeString();

    clockElement.innerText = timeString;
}


function renderCards() {
    container.innerHTML = "";

    items.forEach(item => {
        const card = document.createElement('div');
        card.className = 'card';
        if (item.is_dangerous === true) {
            card.classList.add('danger-mode');
        }
        card.innerHTML = `
        <div class="card-badge">Сектор ${item.storage_sector}</div>
        <h3 class="card-title">${item.name}</h3>
        <p class="card-description">Вес объекта: ${item.weight} кг.</p>
        <div class="card-stats">
            <span>📦 Кол-во : <b>${item.quantity}</b></span>
            <span class="card-extra">${item.is_dangerous ? '⚠️ Опасно': '✅ Безопасно'}</span>
        </div>
        <button class="btn-more">Подробнее</button> 
    `;
    if (item.is_dangerous) {
        const title = card.querySelector('.card-title');
        title.style.color = "red";

    }
    container.appendChild(card)
    });
}

renderCards()

setInterval(updateTime,1000)