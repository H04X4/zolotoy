document.addEventListener('DOMContentLoaded', function () {
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    const removeFromCartButtons = document.querySelectorAll('.remove-from-cart');
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    function showNotification(message, type = 'success') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        document.body.appendChild(notification);
        setTimeout(() => notification.remove(), 3000);
    }

    addToCartButtons.forEach(button => {
        button.addEventListener('click', function () {
            const row = this.closest('tr');
            const productId = row.dataset.productId;
            const quantity = row.querySelector('.quantity-input').value;
            const comment = row.querySelector('.comment-input').value;
            const addToCartUrl = document.querySelector('table').dataset.addToCartUrl;

            button.disabled = true;
            row.classList.add('loading');
            fetch(addToCartUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken,
                },
                body: `product_id=${encodeURIComponent(productId)}&quantity=${encodeURIComponent(quantity)}&comment=${encodeURIComponent(comment)}`
            })
            .then(response => response.json())
            .then(data => {
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
                showNotification('Ошибка: ' + error, 'error');
                button.disabled = false;
                row.classList.remove('loading');
            });
        });
    });

    removeFromCartButtons.forEach(button => {
        button.addEventListener('click', function () {
            const row = this.closest('tr');
            const cartItemId = row.dataset.cartItemId;
            const removeFromCartUrl = document.querySelector('table').dataset.removeFromCartUrl;

            button.disabled = true;
            row.classList.add('loading');
            fetch(removeFromCartUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken,
                },
                body: `cart_item_id=${cartItemId}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    showNotification(data.error, 'error');
                    button.disabled = false;
                    row.classList.remove('loading');
                    return;
                }
                row.remove();
                document.querySelector('#total-sum').textContent = data.total_sum.toFixed(2);
                showNotification(data.success);
                button.disabled = false;
                row.classList.remove('loading');
            })
            .catch(error => {
                showNotification('Ошибка: ' + error, 'error');
                button.disabled = false;
                row.classList.remove('loading');
            });
        });
    });
});