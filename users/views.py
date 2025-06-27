
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import LoginForm, RegisterForm
from django.urls import reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from .token import account_activation_token
from .models import CustomUser
from django.contrib.auth import login


# Create your views here.

class LoginUser(LoginView):
    authentication_form = LoginForm
    template_name = 'users/login.html'
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        next_url = self.request.GET.get('next')
        if next_url:
            context['next'] = next_url
        return context


class RegisterUser(CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your account'
        message = render_to_string('users/activation_mail.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        }
                                   )
        to_email = form.cleaned_data.get('email')

        email = EmailMessage(mail_subject, message, to=[to_email])
        email.content_subtype = "html"
        email.send()
        return HttpResponse('Please confirm your email address to complete the registration')
    def get_success_url(self):
        return reverse_lazy('courses:index')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.backend = 'users.auth_backends.UsernameOrEmailBackend'
        user.save()
        login(request, user)
        return HttpResponse('Thank you for your email confirmation.')
    else:
        return HttpResponse('Activation link is invalid!')



class LogoutUser(LogoutView):

    def get_success_url(self):
        return reverse_lazy('courses:index')

def confirm_mail(request):
    return render(request, 'users/confirm-mail.html')
