from django.shortcuts import render

# Create your views here.
def index(request):
    return render (request, "app/index.html")

def contact(request):
    return render (request,"app/contact.html")

def destination(request):
    return render (request,"app/destination.html")

def pricing(request):
    return render (request,"app/pricing.html")