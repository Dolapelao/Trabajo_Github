from django.urls import path
from .views import *

urlpatterns = [
    path('app/index/',index, name='index'),
    path('', index, name='index'),
    path('app/contact/', contact, name='contact'),
    path('app/destination/', destination, name='destination'),
    path('app/pricing/', pricing, name='pricing'),    
    path('login/', login_user, name='login'),
    path('register/', register, name='register'),
    path('logout/', cerrar_sesion, name='logout'),
    path('reservas', admin_reservas, name='admin_reservas')
]
