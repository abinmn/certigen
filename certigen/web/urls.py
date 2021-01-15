from django.urls import path
from .views import accounts
from .views import dashboard
from .views import event
from .views import email

urlpatterns = [
    path('login', accounts.SignInView.as_view(), name='login'),
    path('', dashboard.DashboardView.as_view(), name='dashboard'),
    path('events', event.EventListView.as_view(), name='events'),
    path('events/create', event.EventCreateView.as_view(), name='events-create'),

    path('emails', email.EmailListView.as_view(), name='emails'),
    path('emails/create', email.EmailCreateView.as_view(), name='email-create'),
    path('emails/<int:pk>', email.EmailSendVeiw.as_view(), name='email-send'),
    path('emails/<int:pk>/update', email.EmailUpdateView.as_view(), name='email-update'),
    path('emails/<int:pk>/delete', email.EmailDeleteView.as_view(), name='email-delete'),
    path('api/emails/<int:pk>', email.EmailDetailsApiView.as_view(), name='email-api-get'),
]