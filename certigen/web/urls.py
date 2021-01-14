from django.urls import path
from .views import accounts
from .views import dashboard
from .views import events

urlpatterns = [
    path('login', accounts.SignInView.as_view(), name='login'),
    path('', dashboard.DashboardView.as_view(), name='dashboard'),
    path('events', events.EventListView.as_view(), name='events'),
    path('events/create', events.EventCreateView.as_view(), name='events-create'),
    path('emails', dashboard.DashboardView.as_view(), name='emails'),
]