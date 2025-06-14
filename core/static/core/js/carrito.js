let cart = [];

// Función para agregar una suscripción al carrito
// Función para agregar una suscripción al carrito
function addToCart(subscription) {
    // Verificar si ya hay una suscripción en el carrito
    if (cart.length === 0) {
        cart.push({ ...subscription, quantity: 1 });  // Agregar la suscripción con cantidad 1
    } else {
        // Reemplazar la suscripción existente
        cart = [{ ...subscription, quantity: 1 }];
    }
    updateCart();
    saveCart();
}

// Función para eliminar una suscripción del carrito por nombre
function removeFromCart(subscriptionName) {
    const itemIndex = cart.findIndex(item => item.name === subscriptionName);
    if (itemIndex !== -1) {
        cart.splice(itemIndex, 1); // Eliminar el artículo del carrito
        updateCart();
        saveCart();
    }
}

// Función para actualizar la visualización del carrito
function updateCart() {
    const cartItemsElement = document.getElementById('cart-items');
    let cartTotal = 0;

    // Limpiar la lista de elementos del carrito
    cartItemsElement.innerHTML = '';

    // Recorrer todas las suscripciones en el carrito
    cart.forEach(item => {
        const { sku, name, price, quantity } = item;
        const totalPrice = price * quantity;
        cartTotal += totalPrice;

        // Crear elemento de lista para la suscripción
        const listItem = document.createElement('li');
        listItem.className = 'list-group-item d-flex justify-content-between lh-sm';
        listItem.innerHTML = `
        <div>
            <h6 class="my-0">${name}</h6>
            <small class="text-muted">SKU: ${sku} | Cantidad: ${quantity}</small>
        </div>
        <span class="text-muted">$${totalPrice.toFixed(2)}</span>
        <button class="btn btn-sm btn-outline-danger remove-item" data-name="${name}">Eliminar</button>`;
        cartItemsElement.appendChild(listItem);

        // Agregar evento al botón de eliminar
        listItem.querySelector('.remove-item').addEventListener('click', () => {
            removeFromCart(name);
        });
    });

    // Actualizar el total del carrito
    document.getElementById('cart-total').textContent = cartTotal.toFixed(2);

    // Mostrar el botón de eliminar del carrito si hay elementos
    const removeButton = document.querySelector('.remove-from-cart');
    if (cart.length > 0) {
        removeButton.classList.remove('d-none');
    } else {
        removeButton.classList.add('d-none');
    }
}

// Función para guardar el carrito en localStorage
function saveCart() {
    localStorage.setItem('cart', JSON.stringify(cart));
}

// Función para cargar el carrito desde localStorage
function loadCart() {
    const cartData = localStorage.getItem('cart');
    if (cartData) {
        cart = JSON.parse(cartData);
        updateCart();
    }
}

// Evento al cargar la página para cargar el carrito guardado
document.addEventListener('DOMContentLoaded', () => {
    loadCart();
});

// Agregar eventos a los botones de agregar al carrito
document.querySelectorAll('.add-to-cart').forEach(button => {
    button.addEventListener('click', () => {
        const sku = button.getAttribute('data-sku'); // nuevo
        const name = button.getAttribute('data-name');
        const price = parseFloat(button.getAttribute('data-price'));
        addToCart({ sku, name, price }); // agrega el SKU al objeto
    });
});
// Evento para el botón de proceder al pago
document.getElementById('checkout-button').addEventListener('click', () => {
    alert('Implementar la lógica para proceder al pago aquí...');
});

// Función para vaciar el carrito
function clearCart() {
    cart = [];
    updateCart();
    saveCart();
}