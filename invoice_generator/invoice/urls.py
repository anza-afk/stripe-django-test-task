from django.urls import path
from . import views

urlpatterns = [
    path('item/<int:id>',views.InvoiceView.as_view(template_name='index.html'), name='invoice'),  
    path('buy/<int:id>', views.SessionView.as_view(), name='session'),
]
