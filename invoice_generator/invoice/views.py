from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, JsonResponse
from .models import Item
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY
PUBLIC_KEY = settings.STRIPE_PUBLIC_KEY

def get_session_id(request: HttpRequest, id: int) -> JsonResponse:
    """API endpoind returning stripe session id"""
    item = Item.objects.get(id=id)
    item_price = item.price
    quantity=request.GET.get('quantity', 1)
    checkout_session = stripe.checkout.Session.create(
        cancel_url='https://example.com/cancel',
        success_url='https://example.com/success',
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
    context = {
        'stripe_pk': PUBLIC_KEY,
        'item': item
    }
    return render(request, 'index.html', context=context)
