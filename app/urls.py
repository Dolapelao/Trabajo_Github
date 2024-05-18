from django.urls import path
from .views import index, contact, destination, pricing

urlpatterns = [
    path('app/index/',index, name='index'),
    path('', index, name='index'),
    path('app/contact/', contact, name='contact'),
    path('app/destination/', destination, name='destination'),
    path('app/pricing/', pricing, name='pricing'),    
]
