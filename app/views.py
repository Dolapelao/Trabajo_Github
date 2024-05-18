from django.shortcuts import render, redirect
from .forms import *

# Create your views here.
def index(request):
    reservaForm = ReservaForm()
    reserva = Reserva.objects.all()
    destinos = Destino.objects.all()
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ReservaForm()
    return render (request, "app/index.html", {'reserva': reserva, 'reservaForm': reservaForm , 'destinos': destinos})

def contact(request):
    contactForm = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ContactForm()
    return render (request, "app/contact.html", {'contactForm': contactForm})

def destination(request):
    return render (request,"app/destination.html")

def pricing(request):
    return render (request,"app/pricing.html")