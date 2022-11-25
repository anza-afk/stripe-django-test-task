from django import forms
from .models import Item, Tax, Discount


class OrderForm(forms.Form):
    items = forms.ModelMultipleChoiceField(
        queryset=Item.objects.all(),
        label='Items',
        widget=forms.CheckboxSelectMultiple(),
        required=False
        )
    discount = forms.ModelChoiceField(
        Discount.objects.all(),
        label='Discount:',
        widget=forms.Select(attrs={
            'style': 'width: 300px;',
            'class': 'form-control'
            }),
        required=False
        )
    tax = forms.ModelChoiceField(
        Tax.objects.all(),
        label='Tax:',
        widget=forms.Select(attrs={
            'style': 'width: 300px;',
            'class': 'form-control'
            }),
        required=False
        )

    def send_order(self):

        pass
