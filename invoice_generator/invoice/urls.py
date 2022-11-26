from django.urls import path
from . import views

urlpatterns = [
    path('create_order', views.OrderFormView.as_view(
        template_name='create_order.html'), name='create_order'),
    path('item/<int:id>', views.InvoiceView.as_view(
        template_name='item.html'), name='invoice'),
    path('order/<int:id>', views.OrderView.as_view(
        template_name='order.html'), name='order_invoice'),
    path('buy/<int:id>', views.SessionView.as_view(), name='session'),
    path('payment-intent/<id>/', views.IntentView.as_view(), name='payment-intent'),
    path('webhooks/stripe/', views.stripe_webhook, name='stripe-webhook'),
]
