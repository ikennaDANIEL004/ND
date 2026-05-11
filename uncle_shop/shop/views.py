from django.conf import settings
from django.core.mail import send_mail
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
        subject = f"New website enquiry from {name}"
        body = (
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Phone: {phone}\n\n"
            f"Message:\n{message}"
        )
        send_mail(
            subject,
            body,
            getattr(settings, 'DEFAULT_FROM_EMAIL', 'info@causeofjoybuilders.com'),
            ['ndubueze77@yahoo.com'],
            fail_silently=True,
        )
        messages.success(request, "Thank you. Your message has been received.")
        return redirect('contact')

    return render(request, 'shop/contact.html')


def why_us(request):
    return render(request, 'shop/why_us.html')
