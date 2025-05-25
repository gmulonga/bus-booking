from django.urls import path
from . import views

urlpatterns = [
    path('', views.booking_list, name='booking-list'),
    path('<int:id>/', views.booking_detail, name='booking-detail'),
    path('create/', views.booking_create, name='booking-create'),
    path('update/<int:id>/', views.booking_update, name='booking-update'),
    path('delete/<int:id>/', views.booking_delete, name='booking-delete'),
]
