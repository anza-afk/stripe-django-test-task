from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, JsonResponse
from .models import Item
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

domain_url = 'http://127.0.0.1:8000/item/'

from django.views.generic import TemplateView, View


class SessionView(View):
    
    def get(self, request, *args, **kwargs):
        item = Item.objects.get(id=self.kwargs['id'])
        quantity = request.GET.get('quantity', 1)

        checkout_session = stripe.checkout.Session.create(
            cancel_url=f'{domain_url}{item.id}?payment_status=cancel',
            success_url=f'{domain_url}{item.id}?payment_status=success',
            mode = 'payment',
            line_items=[
                {
                    'price': item.price,
                    'quantity': quantity
                },
            ]
            )
        return JsonResponse({'session_id': checkout_session.id})


class InvoiceView(TemplateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stripe_pk'] = settings.STRIPE_PUBLIC_KEY
        context['item'] = Item.objects.get(id=self.kwargs['id'])
        context['payment_status'] = self.request.GET.get('payment_status')
        context['quantity'] = self.request.GET.get('quantity', 1)
        print(context)
        return context
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
