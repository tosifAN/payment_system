from django.urls import path
from . import views

urlpatterns = [
    path('create-payment/', views.create_payment, name='create_payment'),
    path('pay/', views.payment_form, name='payment_form'),
    path('home/',views.home,name='home'),
]
