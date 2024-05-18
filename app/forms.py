from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User

class ReservaForm(ModelForm):
    class Meta:
        model = Reserva
        fields = ['nombre', 'actividad', 'destino', 'fecha_viaje']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'actividad': forms.Select(attrs={'class': 'form-control'}),
            'destino': forms.Select(attrs={'class': 'form-control'}),
            'fecha_viaje': forms.DateInput(attrs={'class': 'form-control'}),
        }

class ContactForm(ModelForm):
    class Meta:
        model = Contacto
        fields = ['nombre', 'email', 'asunto', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'asunto': forms.TextInput(attrs={'class': 'form-control'}),
            'mensaje': forms.Textarea(attrs={'class': 'form-control'}),
        }

class RegistroForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']