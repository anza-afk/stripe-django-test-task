from django.db import models

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length = 100)
    description = models.TextField(max_length = 500)
    price = models.CharField(max_length = 100)

    def __str__(self):
        return f'(id:{self.id}) {self.name}'
