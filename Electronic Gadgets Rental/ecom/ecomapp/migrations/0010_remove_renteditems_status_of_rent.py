# Generated by Django 4.1.7 on 2023-03-23 06:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0009_rename_product_id_renteditems_product_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='renteditems',
            name='status_of_rent',
        ),
    ]
