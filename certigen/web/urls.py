from django.urls import path
from .views import accounts

urlpatterns = [
    path('login', accounts.SignInView.as_view(), name='login'),
    path('dashboard', accounts.SignInView.as_view(), name='dashboard'),
]