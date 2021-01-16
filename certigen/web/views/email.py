from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.urls import reverse

from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse

from web.models import Email
from web.forms import SendIndividualEmailForm
from web.aws.sns import AwsSNS

class EmailListView(ListView):
    model = Email
    template_name = 'email/email_list.html'
    context_object_name = 'emails'


class EmailSendVeiw(View):

    form_class = SendIndividualEmailForm
    template_name = 'email/email_send.html'
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            recipient_email = form.cleaned_data['email']
            template_id = kwargs.get('pk')

            if template_id:
                sns = AwsSNS()
                sns.send_email(template_id, [recipient_email])
            return redirect(reverse('emails'))

        return render(request, self.template_name, {'form': form})

    

class EmailCreateView(CreateView):
    model = Email
    fields = ['subject', 'body_plain_text', 'body_html_text', 'attachment', 'event']
    template_name = 'email/email_create_update.html'

    def get_success_url(self):
        return reverse('email-update', args=(self.object.id, ))


class EmailUpdateView(UpdateView):
    model = Email
    fields = ['subject', 'body_plain_text', 'body_html_text', 'attachment', 'event']
    template_name = 'email/email_create_update.html'
    context_object_name = 'email'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_email'] = True
        return context

    def get_success_url(self):
        return reverse('emails')


class EmailDeleteView(DeleteView):
    model = Email
    template_name = 'email/email_delete.html'
    context_object_name = 'email'

    def get_success_url(self):
        return reverse('emails')


class EmailDetailsApiView(View):
    def get(self, request, *args, **kwargs):
        email = Email.objects.get(pk=kwargs.get('pk'))
        data = {
            'id': email.id,
            'subject': email.subject,
            'body_plain_text': email.body_plain_text,
            'body_html_text': email.body_html_text,
        }

        if email.attachment:
            data['attachment'] = email.atttachment.path
        return JsonResponse(data)