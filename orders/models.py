from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    article = models.CharField(max_length=100, unique=True, verbose_name='Артикул')
    image = models.CharField(max_length=255, blank=True, verbose_name='Изображение')
    stock = models.IntegerField(verbose_name='Остаток')
    store_presence = models.CharField(max_length=255, verbose_name='Наличие в магазинах')
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Себестоимость')
    order_quantity = models.IntegerField(default=0, verbose_name='Количество для заказа')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    unique_number = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return self.article

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        
        
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    unique_number = models.IntegerField(unique=True, editable=False)

    def __str__(self):
        return f"{self.user.username} - {self.unique_number}"

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"
        
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    comment = models.TextField(blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.article} ({self.quantity})"

    class Meta:
        unique_together = ('user', 'product')