from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    price = models.CharField(
        max_length=100,
        unique=True
        )

    def __str__(self):
        return self.name


class Discount(models.Model):
    value = models.FloatField()

    class Meta:
        verbose_name = 'Discount'
        verbose_name_plural = 'Discount'

    def __str__(self):
        return f'{self.value}%'


class Tax(models.Model):
    rate = models.FloatField()
    stripe_id = models.CharField(
        max_length=100,
        unique=True
        )

    class Meta:
        verbose_name = 'Tax'
        verbose_name_plural = 'Tax'

    def __str__(self):
        return f'{self.rate}%'


class Order(models.Model):
    item = models.ManyToManyField(
        Item,
        verbose_name='Item'
    )
    tax = models.ForeignKey(
        Tax,
        null=True,
        default=None,
        on_delete=models.SET_DEFAULT
    )
    discount = models.ForeignKey(
        Discount,
        null=True,
        default=None,
        on_delete=models.SET_DEFAULT
    )
    order_created = models.DateTimeField(
        null=True,
        default=None
        )

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Order'
