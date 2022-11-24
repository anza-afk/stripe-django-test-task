import stripe
from django.http import JsonResponse
from django.conf import settings
from django.views.generic import TemplateView, View
from .forms import OrderForm
from .models import Item, Order



stripe.api_key = settings.STRIPE_SECRET_KEY

domain_url = 'http://127.0.0.1:8000/item/'


class SessionView(View):

    def get(self, request, *args, **kwargs):
        line_items = []
        if self.kwargs['id']:
            item = Item.objects.get(id=self.kwargs['id'])
            quantity = request.GET.get('quantity', 1)
            line_items.append({
                'price': item.price,
                'quantity': quantity
                })
        else:

            for id in self.request.GET.getlist('id'):
                try:
                    item = Item.objects.get(id=id)
                    line_items.append({
                        'price': item.price,
                        'quantity': 1   ##########
                        })
                except Item.DoesNotExist:
                    print(item)
        checkout_session = stripe.checkout.Session.create(
            cancel_url=f'{domain_url}{item.id}?payment_status=cancel',
            success_url=f'{domain_url}{item.id}?payment_status=success',
            mode='payment',
            line_items=line_items
            )
        return JsonResponse({'session_id': checkout_session.id})


class InvoiceView(TemplateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stripe_pk'] = settings.STRIPE_PUBLIC_KEY
        context['item'] = Item.objects.get(id=self.kwargs['id'])
        context['quantity'] = self.request.GET.get('quantity', 1)
        context['payment_status'] = self.request.GET.get('payment_status')
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class OrderView(TemplateView):



    def get_context_data(self, **kwargs):
        items = [Item.objects.get(id=order_id) for order_id in self.request.GET.getlist('id')]
        context = super().get_context_data(**kwargs)
        context['stripe_pk'] = settings.STRIPE_PUBLIC_KEY
        context['items'] = items
        context['payment_status'] = self.request.GET.get('payment_status')
        context['quantity'] = self.request.GET.get('quantity', 1)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
