from django.shortcuts import render, redirect
from .models import Product, Service, ContactSubmission
from django.contrib import messages

def home(request):
    products = Product.objects.all()
    services = Service.objects.all()
    return render(request, 'shop/home.html', {'products': products, 'services': services})

def about(request):
    return render(request, 'shop/about.html')

def services(request):
    services_list = Service.objects.all()
    return render(request, 'shop/services.html', {'services': services_list})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        ContactSubmission.objects.create(name=name, email=email, phone=phone, message=message)
        messages.success(request, "Your message has been sent!")
        return redirect('contact')

    return render(request, 'shop/contact.html')