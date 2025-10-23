from django.shortcuts import render

# App/authentication/views.py
from django.http import HttpResponse

def index(request):
    return HttpResponse("Página inicial funcionando!")
