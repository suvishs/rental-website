# Generated by Django 4.1.7 on 2023-03-17 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0003_rename_product_id_cart_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='user_id',
            new_name='user',
        ),
    ]
