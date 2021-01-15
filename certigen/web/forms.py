from django import forms


class SendIndividualEmailForm(forms.Form):
    email = forms.EmailField()