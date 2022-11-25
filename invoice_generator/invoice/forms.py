from django import forms
from .models import Item


class OrderForm(forms.Form):
    item_choices = Item.objects.all().values_list('name', 'name')
    items = forms.MultipleChoiceField(
        label='Получатели:',
        choices=item_choices,
        widget=forms.CheckboxInput(
            attrs={'style': 'width: 300px;', 'class': 'form-control'}
            )
        )
