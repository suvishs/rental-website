# Generated by Django 4.1.7 on 2023-03-20 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0007_customer_application2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='application2',
        ),
    ]