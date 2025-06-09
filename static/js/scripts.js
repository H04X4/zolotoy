document.addEventListener('DOMContentLoaded', function () {
    console.log('scripts.js loaded');
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    const removeFromCartButtons = document.querySelectorAll('.remove-from-cart');
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]')?.value;
    const table = document.querySelector('table');

    if (!csrfToken) {
        console.error('CSRF token not found');
        alert('Ошибка: CSRF-токен отсутствует');
        return;
    }

    if (!table) {
        console.error('Table element not found');
        return;
    }

    function showNotification(message, type = 'success') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        document.body.appendChild(notification);
        setTimeout(() => notification.remove(), 3000);
    }

    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('Add to cart clicked');
            const row = button.closest('tr');
            const productId = button.dataset.productId || row.dataset.productId;
            const quantityInput = row.querySelector('.quantity-input');
            const commentInput = row.querySelector('.comment-input');
            const addToCartUrl = table.dataset.addToCartUrl;

            if (!productId || !quantityInput || !addToCartUrl) {
                console.error('Missing data:', { productId, quantityInput, addToCartUrl });
                showNotification('Ошибка: данные не найдены', 'error');
                return;
            }

            const quantity = parseInt(quantityInput.value) || 1;
            const comment = commentInput ? commentInput.value.trim() : '';

            button.disabled = true;
            row.classList.add('loading');
            fetch(addToCartUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken
                },
                body: `product_id=${encodeURIComponent(productId)}&quantity=${encodeURIComponent(quantity)}&comment=${encodeURIComponent(comment)}`
            })
            .then(response => {
                console.log('Response status:', response.status);
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                return response.json();
            })
            .then(data => {
                console.log('Response data:', data);
                if (data.error) {
                    showNotification(data.error, 'error');
                    return;
                }
                row.remove();
                showNotification(data.success);
                button.disabled = false;
                row.classList.remove('loading');
            })
            .catch(error => {
                console.error('Fetch error:', error);
                showNotification('Ошибка: ' + error.message, 'error');
                button.disabled = false;
                row.classList.remove('loading');
            });
        });
    });

    removeFromCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('Remove from cart clicked');
            const row = this.closest('tr');
            const cartItemId = row.dataset.rowId;
            const removeFromCartUrl = table.dataset.removeFromCart;

            if (!cartItemId || !removeFromCartUrl) {
                console.error('Missing data:', { cartItemId, removeFromCartUrl });
                showNotification('Ошибка: данные не найдены', 'error');
                return;
            }

            button.disabled = true;
            row.classList.add('loading');
            fetch(removeFromCartUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken
                },
                body: `cart_item_id=${encodeURIComponent(cartItemId)}`
            })
            .then(response => {
                console.log('Response status:', response.status);
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                return response.json();
            })
            .then(data => {
                console.log('Response data:', data);
                if (data.error) {
                    showNotification(data.error, 'error');
                    return;
                }
                row.remove();
                const totalSum = document.querySelector('#total-sum');
                if (totalSum) {
                    totalSum.textContent = data.total_sum.toFixed(2);
                }
                showNotification(data.success);
                button.disabled = false;
                row.classList.remove('loading');
            })
            .catch(error => {
                console.error('Fetch error:', error);
                showNotification('Ошибка: ' + error.message, 'error');
                button.disabled = false;
                row.classList.remove('loading');
            });
        });
    });
});