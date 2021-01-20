from django import forms


class SendIndividualEmailForm(forms.Form):
    email = forms.EmailField()


class UploadFileForm(forms.Form):
    file = forms.FileField()