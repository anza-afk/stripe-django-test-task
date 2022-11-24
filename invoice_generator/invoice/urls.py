from django.urls import path
from . import views

urlpatterns = [
    path('item/<int:id>', views.InvoiceView.as_view(template_name='index.html'), name='invoice'),
    path('order', views.OrderView.as_view(template_name='index.html'), name='order_invoice'),
    path('buy', views.SessionView.as_view(), {'id': None}, name='session'),
    path('buy/<int:id>', views.SessionView.as_view(), name='session'),
]
