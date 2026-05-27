const userId = localStorage.getItem('warehouse_user_id');
const container = document.getElementById('cart-container');
const emptyMsg = document.getElementById('empty-msg');


async function loadCart() {
    if (!userId) return;

    const API_URL = `http://127.0.0.1:8000/cart?user_id=${userId}`;
    
    try {
        const response = await fetch(API_URL);
        const cartData = await response.json();
        // Сервер возвращает массив объектов (JOIN items)
        if (!cartData || cartData.length === 0) {
            emptyMsg.style.display = 'block';
            return;
        }
        renderCart(cartData);
    } catch (error) {
        console.error("Ошибка при загрузке корзины:", error);
    }
}

async function renderCart(cartData) {
    container.innerHTML = "";

    // cartData — массив объектов из JOIN (items + cart.quantity as cart_quantity)
    for (const item of cartData) {
        const quantity = item.cart_quantity;

        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
            <h3 class="card-title">${item.name}</h3>
            <p>Количество в заказе: <b>${quantity} шт.</b></p>
            <p>Общий вес: ${(item.weight * quantity).toFixed(2)} кг</p>
        `;
        container.appendChild(card);
    }
}

loadCart();