from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    price = models.CharField(max_length=100)

    def __str__(self):
        return f'(id:{self.id}) {self.name}'


class Order(models.Model):
    item = models.ManyToManyField(
        Item,
        verbose_name='Item'
    )

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Order'
