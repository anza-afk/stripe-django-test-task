import stripe
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.urls import reverse
from django.views.generic import TemplateView, View, FormView
from .forms import OrderForm
from .models import Item, Order
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import json

stripe.api_key = settings.STRIPE_SECRET_KEY

domain_url = 'http://127.0.0.1:8000/'


class SessionView(View):

    def get(self, request, *args, **kwargs):
        line_items = []
        if self.request.GET.get('order'):
            order = Order.objects.get(id=self.kwargs['id'])
            tax = [order.tax.stripe_id, ] if order.tax else None
            for item in order.item.all():
                line_items.append({
                    'price': item.price,
                    'quantity': 1,   ##########
                    'tax_rates': tax
                })
            discount = order.discount.coupon_id
            metadata = {
                "order_id": order.id
            }
        else:
            item = Item.objects.get(id=self.kwargs['id'])
            quantity = request.GET.get('quantity', 1)
            line_items.append({
                'price': item.price,
                'quantity': quantity,
            })
            discount = None
            metadata = {
                "item_id": item.id
            }

        checkout_session = stripe.checkout.Session.create(
            cancel_url=f'{domain_url}/create_order',
            success_url=f'{domain_url}/create_order',
            mode='payment',
            line_items=line_items,
            discounts=[{
                'coupon': discount,
            }],
            metadata=metadata
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


class IntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            request_json = json.loads(request.body)
            customer = stripe.Customer.create(email=request_json['email'])
            if self.request.GET.get('order'):
                order = Order.objects.get(id=self.kwargs['id'])
                amount = 0
                for item in order.item.all*():

                    amount += int(stripe.Price.retrieve(item.price))
                metadata = {
                    "order_id": order.id
                }
            else:
                item = Item.objects.get(id=self.kwargs['id'])
                amount = stripe.Price.retrieve(item.price)['unit_amount']
                metadata = {
                    "item_id": item.id
                }
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                customer=customer['id'],
                metadata=metadata
            )
            print(intent['client_secret'])
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)})


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        customer_email = session["customer_details"]["email"]
        if session["metadata"].get("item_id"):
            product_id = session["metadata"]["item_id"]
            order = Item.objects.get(id=product_id)
        elif session["metadata"].get("order_id"):
            product_id = session["metadata"]["order_id"]
            order = Order.objects.get(id=product_id)

        # - send email to the customer
        print(customer_email, order.id)
        #
    elif event["type"] == "payment_intent.succeeded":

        intent = event['data']['object']

        stripe_customer_id = intent["customer"]
        stripe_customer = stripe.Customer.retrieve(stripe_customer_id)

        customer_email = stripe_customer['email']
        if intent["metadata"].get("item_id"):
            product_id = intent["metadata"]["item_id"]
            order = Item.objects.get(id=product_id)
        elif intent["metadata"].get("order_id"):
            product_id = intent["metadata"]["order_id"]
            order = Order.objects.get(id=product_id)
    return HttpResponse(status=200)
