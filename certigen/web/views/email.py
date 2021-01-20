import os

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.urls import reverse

from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse

from web.storage import EmailCsvStorage
from web.models import Email
from web.forms import SendIndividualEmailForm, UploadFileForm
from web.aws.sns import AwsSNS

class EmailListView(ListView):
    model = Email
    template_name = 'email/email_list.html'
    context_object_name = 'emails'


class EmailSendVeiw(View):

    form_class = SendIndividualEmailForm
    template_name = 'email/email_send.html'
    def get(self, request, *args, **kwargs):
        individual_form = self.form_class()
        upload_file_form = UploadFileForm
        template_id = kwargs.get('pk')

        return render(request, self.template_name, {'individual_form': individual_form, 'upload_file_form':upload_file_form, 'template_id':template_id})

    def post(self, request, *args, **kwargs):
        individual_form = self.form_class(request.POST)
        if individual_form.is_valid():
            recipient_email = individual_form.cleaned_data['email']
            template_id = kwargs.get('pk')

            if template_id:
                sns = AwsSNS()
                sns.send_email(template_id, [recipient_email])
            return redirect(reverse('emails'))

        return render(request, self.template_name, {'individual_form': individual_form})

    

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
            data['attachment'] = f'{email.attachment.storage.location}/{email.attachment.name} '
        return JsonResponse(data)


class EmailCSVUploadView(View):
    def post(self, requests, **kwargs):
        file_obj = requests.FILES.get('file', '')
        template_id = requests.POST.get('template_id', '0')
        file_directory_within_bucket = f'recipients/{template_id}'

        file_path_within_bucket = os.path.join(
            file_directory_within_bucket,
            file_obj.name
        )

        media_storage = EmailCsvStorage()

        if not media_storage.exists(file_path_within_bucket): # avoid overwriting existing file
            media_storage.save(file_path_within_bucket, file_obj)
            file_url = media_storage.url(file_path_within_bucket)

            sns = AwsSNS()
            sns.bulk_email_csv(file_path_within_bucket, template_id)
            return redirect(reverse('emails'))
        else:
            return JsonResponse({
                'message': 'Error: file {filename} already exists at {file_directory} in bucket {bucket_name}'.format(
                    filename=file_obj.name,
                    file_directory=file_directory_within_bucket,
                    bucket_name=media_storage.bucket_name
                ),
            }, status=400)