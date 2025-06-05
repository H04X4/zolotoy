$(document).ready(function() {
    $('.order-quantity, .comment').on('change', function() {
        var row = $(this).closest('tr');
        var productId = row.data('product-id');
        var orderQuantity = row.find('.order-quantity').val();
        var comment = row.find('.comment').val();
        var updateUrl = $('table').data('update-url');

        row.addClass('updating');
        $.ajax({
            url: updateUrl,
            type: 'POST',
            data: {
                product_id: productId,
                order_quantity: orderQuantity,
                comment: comment,
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(data) {
                row.find('.line-total').text(data.line_total.toFixed(2));
                $('#total-sum').text(data.total_sum.toFixed(2));
                row.removeClass('updating').addClass('updated');
                setTimeout(() => row.removeClass('updated'), 1000);
            },
            error: function(xhr) {
                row.removeClass('updating');
                alert('Ошибка при обновлении данных: ' + xhr.statusText);
            }
        });
    });
});