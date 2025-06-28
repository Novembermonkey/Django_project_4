from django.shortcuts import redirect
from django.urls import reverse

def require_email(strategy, details, user=None, *args, **kwargs):
    if details.get('email'):
        return
    return redirect(reverse('require_email'))
