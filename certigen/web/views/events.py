from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.urls import reverse

from web.models import Event


class EventListView(ListView):
    model = Event
    template_name = 'events.html'
    context_object_name = 'events'


class EventCreateView(CreateView):
    model = Event
    fields = ['name']
    template_name = 'event_create.html'

    def get_success_url(self):
        return reverse('events')


class EventDetailsView(DetailView):
    model = Event
    template_name = 'event_details.html'