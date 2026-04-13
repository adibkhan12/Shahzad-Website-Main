from django.shortcuts import render


def about(request):
    return render(request, "core/about.html")


def terms(request):
    return render(request, "core/terms.html")


def support(request):
    return render(request, "core/support.html")
