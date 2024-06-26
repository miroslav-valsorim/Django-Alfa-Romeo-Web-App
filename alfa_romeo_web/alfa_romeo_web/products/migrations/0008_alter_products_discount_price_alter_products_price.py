# Generated by Django 5.0.3 on 2024-05-23 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_products_discount_price_alter_products_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='discount_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='products',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
