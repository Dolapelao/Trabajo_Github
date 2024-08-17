
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponse
from django.db.models import Q
from django.utils.timezone import make_aware
from datetime import datetime

# Create your views here.
@login_required(login_url='/login')
def index(request):
    reservaForm = ReservaForm()
    reserva = Reserva.objects.all()
    destinos = Destino.objects.all().order_by('nombre')
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
    reserva = Reserva.objects.all().order_by('-fecha_viaje')
    reservas_este_mes = Reserva.reservas_este_mes()
    if "generar_reporte" in request.GET:
        mes_seleccionado = int(request.GET.get('mes'))
        año_actual = datetime.now().year
        
        #transformar el mes seleccionado a un nombre
        meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        mes_string = meses[mes_seleccionado - 1]

        # Crear una respuesta del tipo Excel
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename="reporte reservas {mes_string}.xlsx"'

        # Crear un libro y una hoja de Excel
        workbook = xlsxwriter.Workbook(response, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        # Escribir los encabezados
        worksheet.write('A1', 'Nombre de la Reserva')
        worksheet.write('B1', 'Actividad')
        worksheet.write('C1', 'Destino')
        worksheet.write('D1', 'Fecha del Viaje')

        # Filtrar reservas por el mes seleccionado
        inicio_mes = make_aware(datetime(año_actual, mes_seleccionado, 1))
        if mes_seleccionado == 12:
            fin_mes = make_aware(datetime(año_actual + 1, 1, 1))
        else:
            fin_mes = make_aware(datetime(año_actual, mes_seleccionado + 1, 1))

        reservas = Reserva.objects.filter(fecha_viaje__gte=inicio_mes, fecha_viaje__lt=fin_mes)

        # Escribir los datos de las reservas en el Excel
        for idx, reserva in enumerate(reservas, start=1):
            worksheet.write(idx, 0, reserva.nombre)
            worksheet.write(idx, 1, reserva.actividad.nombre)
            worksheet.write(idx, 2, reserva.destino.nombre)
            worksheet.write(idx, 3, str(reserva.fecha_viaje))

        # Cerrar el libro de Excel
        workbook.close()

        return response
    
    if "full_reporte" in request.GET:
        # Crear una respuesta del tipo Excel
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Reporte reservas completas.xlsx"'

        # Crear un libro y una hoja de Excel
        workbook = xlsxwriter.Workbook(response, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        # Aquí puedes definir formatos, como `bold = workbook.add_format({'bold': True})`

        # Escribir los encabezados
        worksheet.write('A1', 'Nombre de la Reserva')
        worksheet.write('B1', 'Actividad')
        worksheet.write('C1', 'Destino')
        worksheet.write('D1', 'Fecha del Viaje')
        # Añadir más columnas según sea necesario

        # Obtener los datos de las reservas (aquí puedes filtrar por mes si es necesario)
        reservas = Reserva.objects.all()

        # Escribir los datos de las reservas en el Excel
        for idx, reserva in enumerate(reservas):
            worksheet.write(idx + 1, 0, reserva.nombre)
            worksheet.write(idx + 1, 1, reserva.actividad.nombre)
            worksheet.write(idx + 1, 2, reserva.destino.nombre)
            worksheet.write(idx + 1, 3, str(reserva.fecha_viaje))
            # Añadir más datos según sea necesario

        # Cerrar el libro de Excel
        workbook.close()

        return response
    else:
        reserva = Reserva.objects.all()
        return render(request, 'app/administrar_reservas.html', {'reservas': reserva, 'reservas_este_mes': reservas_este_mes})

@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def mod_reservas(request, id):
    reserva = Reserva.objects.get(id=id)
    datos={
        'form': ReservaForm(instance=reserva)
    }

    if request.method=='POST':
        formulario = ReservaForm(data=request.POST, instance=reserva)
        if formulario.is_valid():
            formulario.save()
            return redirect('admin_reservas')
    return render(request, 'app/modificar_reserva.html', datos)

@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def form_del_cargo(request, id):
    reserva = Reserva.objects.filter(id=id)
    
    for re in reserva:
        re.delete()
    
    return redirect("admin_reservas")