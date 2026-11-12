
import logging
import re
import hashlib

from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Product, Service, ContactSubmission

logger = logging.getLogger(__name__)


def home(request):
    products = Product.objects.all()
    services = Service.objects.all()
    return render(
        request,
        'shop/home.html',
        {'products': products, 'services': services}
    )


def about(request):
    return render(request, 'shop/about.html')


def services(request):
    services_list = Service.objects.all()
    return render(
        request,
        'shop/services.html',
        {'services': services_list}
    )


def gallery(request):
    return render(request, 'shop/gallery.html')


def get_client_ip(request):
    """
    Get the visitor IP address.
    Uses the proxy-provided address when deployed behind Railway.
    """
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if forwarded_for:
        return forwarded_for.split(',')[0].strip()

    return request.META.get('REMOTE_ADDR', 'unknown')


def contact(request):
    if request.method == 'POST':

        # 1. HONEYPOT PROTECTION
        # Real visitors should leave this hidden field empty.
        honeypot = request.POST.get('website', '').strip()

        if honeypot:
            logger.warning("Contact spam blocked by honeypot.")
            messages.success(
                request,
                "Thank you. Your message has been received."
            )
            return redirect('contact')

        # 2. RATE LIMITING
        ip_address = get_client_ip(request)

        # Hash the IP instead of storing it in the cache key.
        ip_hash = hashlib.sha256(
            ip_address.encode()
        ).hexdigest()

        cache_key = f"contact_rate_limit_{ip_hash}"

        attempts = cache.get(cache_key, 0)

        if attempts >= 3:
            messages.error(
                request,
                "Too many submissions. Please wait 10 minutes before trying again."
            )
            return redirect('contact')

        cache.set(
            cache_key,
            attempts + 1,
            timeout=600
        )

        # 3. COLLECT FORM INFORMATION
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        phone = request.POST.get('phone', '').strip()
        message = request.POST.get('message', '').strip()

        # 4. SERVER-SIDE VALIDATION
        if not all([name, email, phone, message]):
            messages.error(
                request,
                "Please complete all required fields."
            )
            return redirect('contact')

        if len(name) > 200 or len(name) < 2:
            messages.error(
                request,
                "Please enter a valid name."
            )
            return redirect('contact')

        # Allow normal names, including international characters.
        if re.search(r'[\x00-\x1f<>]', name):
            messages.error(
                request,
                "Please enter a valid name."
            )
            return redirect('contact')

        try:
            validate_email(email)
        except ValidationError:
            messages.error(
                request,
                "Please enter a valid email address."
            )
            return redirect('contact')

        if len(phone) > 50 or not re.fullmatch(
            r'[0-9+\s().-]{7,50}', phone
        ):
            messages.error(
                request,
                "Please enter a valid phone number."
            )
            return redirect('contact')

        if len(message) < 20 or len(message) > 5000:
            messages.error(
                request,
                "Your message must contain between 20 and 5000 characters."
            )
            return redirect('contact')

        # 5. DUPLICATE SUBMISSION PROTECTION
        recent_time = timezone.now() - timedelta(minutes=10)

        duplicate = ContactSubmission.objects.filter(
            email__iexact=email,
            message=message,
            created_at__gte=recent_time
        ).exists()

        if duplicate:
            messages.error(
                request,
                "This message has already been submitted. Please wait before sending it again."
            )
            return redirect('contact')

        # 6. SAVE GENUINE SUBMISSION
        submission = ContactSubmission.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message,
        )

        # 7. SEND BUSINESS NOTIFICATION
        subject = f"New contact form message from {name}"

        body = (
            "A new message was submitted from the website contact page.\n\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Phone: {phone}\n\n"
            f"Message:\n{message}"
        )

        recipient = getattr(
            settings,
            'CONTACT_NOTIFICATION_EMAIL',
            'ndubueze77@yahoo.com'
        )

        try:
            notification = EmailMessage(
                subject,
                body,
                getattr(
                    settings,
                    'DEFAULT_FROM_EMAIL',
                    'ndubueze77@yahoo.com'
                ),
                [recipient],
            )

            notification.reply_to = [email]
            notification.send(fail_silently=False)

        except Exception:
            logger.exception(
                "Contact submission %s was saved, but notification email failed.",
                submission.pk,
            )

        messages.success(
            request,
            "Thank you. Your message has been received."
        )

        return redirect('contact')

    return render(request, 'shop/contact.html')


def why_us(request):
    return render(request, 'shop/why_us.html')


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return [
            "home",
            "about",
            "services",
            "gallery",
            "why_us",
            "contact",
        ]

    def location(self, item):
        return reverse(item)


def robots_txt(request):
    content = """User-agent: *
Allow: /

Sitemap: https://causeofjoybuilders.com/sitemap.xml
"""
    return HttpResponse(content, content_type="text/plain")
