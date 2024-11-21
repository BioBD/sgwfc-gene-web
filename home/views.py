from django.shortcuts import render


def home(request):
    """Função da View para página Home"""
    return render(request, 'home/home.html')


def about(request):
    """Função da View para página Sobre"""
    return render(request, 'home/about.html')


def drugstone(request):
    """Função da View para página Home"""
    return render(request, 'front-end/drugstone.html')
