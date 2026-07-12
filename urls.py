from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('appointment', views.appointment, name='appointment'),
    path('payment', views.process_payment, name='payment'),
]
