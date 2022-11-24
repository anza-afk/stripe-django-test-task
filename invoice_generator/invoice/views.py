from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, JsonResponse
from .models import Item
import stripe
from django.conf import settings
import os

stripe.api_key = settings.STRIPE_SECRET_KEY

domain_url = 'http://127.0.0.1:8000/item/'
def get_session_id(request: HttpRequest, id: int) -> JsonResponse:
    """API endpoind returning stripe session id"""
    item = Item.objects.get(id=id)
    item_price = item.price
    quantity = request.GET.get('quantity', 1)

    checkout_session = stripe.checkout.Session.create(
        cancel_url=f'{domain_url}{item.id}?payment_status=cancel',
        success_url=f'{domain_url}{item.id}?payment_status=success',
        mode = 'payment',
        line_items=[
            {
                'price': item_price,
                'quantity': quantity
            },
        ]
        )
    return JsonResponse({'session_id': checkout_session.id})


def get_invoice(request: HttpRequest, id: int):
    item = Item.objects.get(id=id)
    payment_status = request.GET.get('payment_status')
    quantity = request.GET.get('quantity', 1)
    context = {
        'stripe_pk': settings.STRIPE_PUBLIC_KEY,
        'item': item,
        'payment_status': payment_status,
        'quantity': quantity,
    }
    return render(request, 'index.html', context=context)
