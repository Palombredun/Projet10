from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.shortcuts import redirect


def logout(request):
    logout(request)
    return render(request, "core/home.html")
