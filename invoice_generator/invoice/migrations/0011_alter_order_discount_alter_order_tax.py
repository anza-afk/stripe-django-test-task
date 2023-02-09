# Generated by Django 4.1.3 on 2022-11-28 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("invoice", "0010_item_currency"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="discount",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                to="invoice.discount",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="tax",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                to="invoice.tax",
            ),
        ),
    ]