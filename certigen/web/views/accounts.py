from django.contrib.auth.views import LoginView


class SignInView(LoginView):
    template_name = 'login.html'
