# Generated by Django 4.1.3 on 2022-11-25 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("invoice", "0004_discount_tax_alter_item_price_order_discount_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="order_created",
            field=models.DateTimeField(default=None, null=True),
        ),
    ]