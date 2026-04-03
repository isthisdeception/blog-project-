"""
Pages views - Static page views for About, Contact, Newsletter.
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from blog.models import Newsletter
from pages.models import ContactMessage


def about_view(request):
    """About page view."""
    return render(request, 'pages/about.html')


def contact_view(request):
    """Contact page with form handling."""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Save the contact message to the database
        if name and email and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject or '',
                message=message,
            )
        
        messages.success(
            request, 
            f'Thank you {name}! Your message has been received. We\'ll get back to you soon.'
        )
        return redirect('pages:contact')
    
    return render(request, 'pages/contact.html')


def newsletter_subscribe(request):
    """Handle newsletter subscription."""
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            # Check if already subscribed
            if Newsletter.objects.filter(email=email).exists():
                messages.info(request, 'You are already subscribed to our newsletter.')
            else:
                Newsletter.objects.create(email=email)
                messages.success(request, 'Thank you for subscribing to our newsletter!')
    
    return redirect(request.META.get('HTTP_REFERER', 'blog:post-list'))


def custom_404_view(request, exception):
    """Custom 404 page for page not found errors."""
    return render(request, 'pages/404.html', status=404)
