# Generated by Django 4.1.7 on 2023-03-20 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0006_customer_usr'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='application2',
            field=models.BooleanField(default=False),
        ),
    ]