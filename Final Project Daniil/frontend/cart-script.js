const userId = localStorage.getItem('warehouse_user_id');
const container = document.getElementById('cart-container');
const emptyMsg = document.getElementById('empty-msg');


async function loadCart() {
    if (!userId) return;

    const API_URL = `http://127.0.0.1/cart?user_id=${userId}`;
    
    try {
        const response = await fetch(API_URL);
        const cartData = await response.json()
        if (Object.keys(cartData).length === 0)
        {
            emptyMsg.style.display = 'block';
            return;
        }
        renderCards(cartData)
    }catch (error) {
        console.error("Ошибка при загрузке корзины:", error);

    }

}

async function renderCart(cartData) {
    container.innerHTML="";

    for( const itemId in cartData) {
        const quantity = cartData[itemId];
        const res = await fetch(`http://127.0.0.1:8000/items/${itemId}`)
        const item = await res.json();

        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
            <h3 class="card-title">${item.name}</h3>
            <p>Количество в заказе: <b>${quantity} шт.</b></p>
            <p>Общий вес: ${item.weight * quantity} кг</p>
        `;
        container.appendChild(card);

    }
}

loadCart();