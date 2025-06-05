from django.db import models


class Product(models.Model):
    article = models.CharField(max_length=100, unique=True, verbose_name='Артикул')
    image = models.CharField(max_length=255, blank=True, verbose_name='Изображение')
    stock = models.IntegerField(verbose_name='Остаток')
    store_presence = models.CharField(max_length=255, verbose_name='Наличие в магазинах')
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Себестоимость')
    order_quantity = models.IntegerField(default=0, verbose_name='Количество для заказа')
    comment = models.TextField(blank=True, verbose_name='Комментарий')

    def __str__(self):
        return self.article

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        