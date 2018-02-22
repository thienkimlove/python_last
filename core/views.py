# We not using this anymore but keep as example code
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect, resolve_url

def core_logout(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'Bạn đã đăng xuất!')
    return redirect(resolve_url(settings.LOGOUT_REDIRECT_URL))

