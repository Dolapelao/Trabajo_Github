
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import user_passes_test, login_required

# Create your views here.
@login_required(login_url='/login')
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

@login_required(login_url='/login')
def contact(request):
    contactForm = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ContactForm()
    return render (request, "app/contact.html", {'contactForm': contactForm})

@login_required(login_url='/login')
def destination(request):
    return render (request,"app/destination.html")

@login_required(login_url='/login')
def pricing(request):
    return render (request,"app/pricing.html")

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password) 
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
            return render(request, 'app/login.html')
    return render(request, 'app/login.html')

def register(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        username = request.POST['username']
        password = request.POST['confirm-password']
        email = request.POST['email']
        if form.is_valid():
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            login(request, user)
            return redirect('index')
        else: 
            messages.error(request, 'Error al registrar el usuario')
            return render(request, 'app/registro.html')
    return render(request, 'app/registro.html')

def cerrar_sesion(request):
    logout(request)
    if 'username' in request.session:
        del request.session['username']  
    
    return redirect('login') 

@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def admin_reservas(request):
    reserva = Reserva.objects.all()
    return render(request, 'app/administrar_reservas.html', {'reservas': reserva})