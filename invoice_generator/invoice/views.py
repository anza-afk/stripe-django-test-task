import stripe
from django.http import JsonResponse
from django.conf import settings
from django.urls import reverse
from django.views.generic import TemplateView, View, FormView
from .forms import OrderForm
from .models import Item, Order
from datetime import datetime

stripe.api_key = settings.STRIPE_SECRET_KEY

domain_url = 'http://127.0.0.1:8000/'


class SessionView(View):

    def get(self, request, *args, **kwargs):
        line_items = []
        if self.request.GET.get('order'):
            order = Order.objects.get(id=self.kwargs['id'])
            tax = [order.tax.stripe_id, ] if order.tax else None
            print(tax)
            for item in order.item.all():
                line_items.append({
                    'price': item.price,
                    'quantity': 1,   ##########
                    'tax_rates': tax
                })
            discount = order.discount.coupon_id
        else:
            item = Item.objects.get(id=self.kwargs['id'])
            quantity = request.GET.get('quantity', 1)
            line_items.append({
                'price': item.price,
                'quantity': quantity
            })
            discount = None

        checkout_session = stripe.checkout.Session.create(
            cancel_url=f'{domain_url}/create_order',
            success_url=f'{domain_url}/create_order',
            mode='payment',
            line_items=line_items,
            discounts=[{
                'coupon': discount,
            }],
            # tax_id_collection={
            #     'enabled': True,
            # },
            )
        return JsonResponse({'session_id': checkout_session.id})


class InvoiceView(TemplateView):

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
        order = Order.objects.get(id=self.kwargs['id'])
        context = super().get_context_data(**kwargs)
        context['stripe_pk'] = settings.STRIPE_PUBLIC_KEY
        context['order'] = order
        context['items'] = order.item.all()
        context['quantity'] = self.request.GET.get('quantity', 1)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class OrderFormView(FormView):

    form_class = OrderForm

    def form_valid(self, form):
        new_order = Order()
        new_order.tax = form.cleaned_data['tax']
        new_order.discount = form.cleaned_data['discount']
        new_order.save()
        for item in form.cleaned_data['items']:
            new_order.item.add(
                Item.objects.get(id=item.id))
        new_order.order_created = datetime.now()
        new_order.save()
        self.success_url = reverse(
            'order_invoice',
            kwargs={'id': new_order.id}
        )
        return super().form_valid(form)
