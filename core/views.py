from django.shortcuts import render


def home(request):
    return render(request, "core/home.html")


def legale_notice(request):
    return render(request, "core/legale_notice.html")
