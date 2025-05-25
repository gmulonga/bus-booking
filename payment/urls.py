from django.urls import path
from .views import payment_create, payment_list, payment_detail, payment_update, payment_delete

urlpatterns = [
    path('add/', payment_create, name='add_payment'),
    path('get/', payment_list, name='list_payment'),
    path('get/<int:id>/', payment_detail, name='payment_detail'),
    path('update/<int:id>/', payment_update, name='update_payment'),
    path('delete/<int:id>/', payment_delete, name='delete_payment')
]
