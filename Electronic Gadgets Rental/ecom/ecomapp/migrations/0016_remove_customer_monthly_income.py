# Generated by Django 4.1.7 on 2023-03-28 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0015_customer_net_pay'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='monthly_income',
        ),
    ]
