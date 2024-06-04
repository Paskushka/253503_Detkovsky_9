from django.shortcuts import render


def myzei_home(request):
    return render(request, 'main/about.html')
