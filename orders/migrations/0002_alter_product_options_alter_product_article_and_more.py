# Generated by Django 5.2.2 on 2025-06-05 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукты'},
        ),
        migrations.AlterField(
            model_name='product',
            name='article',
            field=models.CharField(max_length=100, unique=True, verbose_name='Артикул'),
        ),
        migrations.AlterField(
            model_name='product',
            name='comment',
            field=models.TextField(blank=True, verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='product',
            name='cost_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Себестоимость'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.CharField(blank=True, max_length=255, verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='product',
            name='order_quantity',
            field=models.IntegerField(default=0, verbose_name='Количество для заказа'),
        ),
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.IntegerField(verbose_name='Остаток'),
        ),
        migrations.AlterField(
            model_name='product',
            name='store_presence',
            field=models.CharField(max_length=255, verbose_name='Наличие в магазинах'),
        ),
    ]
