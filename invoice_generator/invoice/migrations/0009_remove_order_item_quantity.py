# Generated by Django 4.1.3 on 2022-11-26 14:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0008_order_item_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='item_quantity',
        ),
    ]
