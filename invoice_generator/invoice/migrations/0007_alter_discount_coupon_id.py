# Generated by Django 4.1.3 on 2022-11-26 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0006_discount_coupon_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='coupon_id',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
