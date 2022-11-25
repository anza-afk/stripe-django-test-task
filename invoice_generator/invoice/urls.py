from django.urls import path
from . import views

urlpatterns = [
    path('create_order', views.OrderFormView.as_view(
        template_name='create_order.html'), name='create_order'),
    path('item/<int:id>', views.InvoiceView.as_view(
        template_name='item.html'), name='invoice'),
    path('order/<int:id>', views.OrderView.as_view(
        template_name='order.html'), name='order_invoice'),
    # path('buy/<int:order_id>', views.SessionView.as_view(), {'id': None}, name='session'),
    path('buy/<int:id>', views.SessionView.as_view(), name='session'),
]
