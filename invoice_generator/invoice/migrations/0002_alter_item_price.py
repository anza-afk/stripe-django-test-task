# Generated by Django 4.1.3 on 2022-11-23 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("invoice", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item", name="price", field=models.CharField(max_length=100),
        ),
    ]
