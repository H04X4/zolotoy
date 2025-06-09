document.addEventListener('DOMContentLoaded', function () {
    const table = document.querySelector('table[data-update-url]');
    if (!table) return;

    const updateUrl = table.dataset.updateUrl;
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    function updateRow(row, productId, orderQuantity, comment) {
        row.classList.add('updating');
        fetch(updateUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken,
            },
            body: `product_id=${productId}&order_quantity=${orderQuantity}&comment=${encodeURIComponent(comment)}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Ошибка: ' + data.error);
                return;
            }
            row.querySelector('.line-total').textContent = data.line_total.toFixed(2);
            document.getElementById('total-sum').textContent = data.total_sum.toFixed(2);
            row.classList.remove('updating');
            row.classList.add('updated');
            setTimeout(() => row.classList.remove('updated'), 1000);
        })
        .catch(error => {
            alert('Ошибка: ' + error);
            row.classList.remove('updating');
        });
    }

    table.addEventListener('change', function (e) {
        if (e.target.classList.contains('order-quantity') || e.target.classList.contains('comment')) {
            const row = e.target.closest('tr');
            const productId = row.dataset.productId;
            const orderQuantity = row.querySelector('.order-quantity').value;
            const comment = row.querySelector('.comment').value;
            updateRow(row, productId, orderQuantity, comment);
        }
    });
});