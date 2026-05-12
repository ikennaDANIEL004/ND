import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from .models import Product, Service, ContactSubmission

logger = logging.getLogger(__name__)

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
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        message = request.POST.get('message', '').strip()

        submission = ContactSubmission.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message,
        )
        subject = f"New website enquiry from {name}"
        body = (
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Phone: {phone}\n\n"
            f"Message:\n{message}"
        )
        recipient = getattr(settings, 'CONTACT_NOTIFICATION_EMAIL', 'ndubueze77@yahoo.com')
        try:
            send_mail(
                subject,
                body,
                getattr(settings, 'DEFAULT_FROM_EMAIL', 'info@causeofjoybuilders.com'),
                [recipient],
                fail_silently=False,
            )
        except Exception:
            logger.exception(
                "Contact submission %s was saved, but the notification email could not be sent.",
                submission.pk,
            )
        messages.success(request, "Thank you. Your message has been received.")
        return redirect('contact')

    return render(request, 'shop/contact.html')


def why_us(request):
    return render(request, 'shop/why_us.html')
