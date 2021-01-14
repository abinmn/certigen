from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.urls import reverse

from web.models import Email

class EmailListView(ListView):
    model = Email
    template_name = 'email/email_list.html'
    context_object_name = 'emails'


class EmailCreateView(CreateView):
    model = Email
    fields = ['subject', 'body_plain_text', 'body_html_text', 'attachment', 'event']
    template_name = 'email/email_create_update.html'

    def get_success_url(self):
        return reverse('emails')


class EmailUpdateView(UpdateView):
    model = Email
    fields = ['subject', 'body_plain_text', 'body_html_text', 'attachment', 'event']
    template_name = 'email/email_create_update.html'

    def get_success_url(self):
        return reverse('emails')


class EmailDeleteView(DeleteView):
    model = Email
    template_name = 'email/email_delete.html'
    context_object_name = 'email'

    
    def get_success_url(self):
        return reverse('emails')