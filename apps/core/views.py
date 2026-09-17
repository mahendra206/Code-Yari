"""
Core app — Views
Home, About, Contact, Privacy, Terms, Error pages
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator

from .models import SiteSettings, StatItem, TeamMember, ContactMessage
from .forms import ContactForm
from apps.services.models import Service
from apps.portfolio.models import PortfolioProject
from apps.testimonials.models import Testimonial
from apps.blog.models import BlogPost


def home(request):
    """Homepage view with all dynamic sections."""
    featured_services = Service.objects.filter(
        is_active=True, is_featured=True
    ).order_by('order')[:6]

    all_services = Service.objects.filter(is_active=True).order_by('order')[:12]

    featured_portfolio = PortfolioProject.objects.filter(
        published=True, featured=True
    ).select_related('category').order_by('-completion_date')[:6]

    featured_testimonials = Testimonial.objects.filter(
        published=True, featured=True
    ).order_by('order')[:6]

    recent_posts = BlogPost.objects.filter(
        published=True
    ).select_related('category', 'author').order_by('-published_date')[:3]

    stats = StatItem.objects.filter(is_active=True).order_by('order')

    context = {
        'page_title': 'Code Yari — Code. Create. Grow.',
        'meta_description': 'Code Yari is a young digital technology team building websites, apps, SEO, digital marketing, UI/UX, AI and automation solutions to grow your business online.',
        'featured_services': featured_services,
        'all_services': all_services,
        'featured_portfolio': featured_portfolio,
        'featured_testimonials': featured_testimonials,
        'recent_posts': recent_posts,
        'stats': stats,
    }
    return render(request, 'core/home.html', context)


def about(request):
    """About page — company story, philosophy, mission, vision."""
    context = {
        'page_title': 'About Us — Code Yari | Digital Agency & Technology Partner',
        'meta_description': 'Learn about Code Yari — our philosophy, core pillars, and how we help businesses grow online.',
    }
    return render(request, 'core/about.html', context)


def team(request):
    """Dedicated Our Team page — team members and culture."""
    team_members = TeamMember.objects.filter(is_active=True).order_by('order')
    context = {
        'page_title': 'Our Team — Code Yari | Meet The Minds',
        'meta_description': 'Meet the talented team of developers, designers, and growth specialists behind Code Yari.',
        'team_members': team_members,
    }
    return render(request, 'core/team.html', context)


@require_http_methods(["GET", "POST"])
def contact(request):
    """Contact page with form submission."""
    if request.method == 'POST':
        form = ContactForm(request.POST)

        # Basic spam protection: check honeypot field
        if request.POST.get('website'):
            messages.warning(request, 'Spam detected.')
            return redirect('core:contact')

        if form.is_valid():
            # Save to database
            msg = ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data.get('phone', ''),
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message'],
                ip_address=_get_client_ip(request),
            )

            # Send email notification (if configured)
            _send_contact_notification(form.cleaned_data)
            _send_contact_confirmation(form.cleaned_data)

            messages.success(
                request,
                f"Thank you, {form.cleaned_data['name']}! Your message has been sent. We'll get back to you within 24 hours."
            )
            return redirect('core:contact')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()

    context = {
        'page_title': 'Contact Us — Code Yari',
        'meta_description': 'Get in touch with Code Yari. We\'d love to hear about your project and help your business grow online.',
        'form': form,
    }
    return render(request, 'core/contact.html', context)


def privacy_policy(request):
    context = {
        'page_title': 'Privacy Policy — Code Yari',
        'meta_description': 'Code Yari Privacy Policy — Learn how we collect, use, and protect your personal information.',
    }
    return render(request, 'core/privacy_policy.html', context)


def terms_conditions(request):
    context = {
        'page_title': 'Terms & Conditions — Code Yari',
        'meta_description': 'Code Yari Terms & Conditions — Please read our terms of service before using our services.',
    }
    return render(request, 'core/terms_conditions.html', context)


def robots_txt(request):
    """Serve robots.txt dynamically."""
    content = render_to_string('core/robots.txt', {'site_url': settings.SITE_URL})
    from django.http import HttpResponse
    return HttpResponse(content, content_type='text/plain')


def error_404(request, exception=None):
    return render(request, 'errors/404.html', status=404)


def error_500(request):
    return render(request, 'errors/500.html', status=500)


# ── Helpers ────────────────────────────────────────────────────────────────────

def _get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def _send_contact_notification(data):
    """Send new contact message notification to admin."""
    try:
        send_mail(
            subject=f"New Contact: {data['subject']}",
            message=f"Name: {data['name']}\nEmail: {data['email']}\nPhone: {data.get('phone', 'N/A')}\n\nMessage:\n{data['message']}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=True,
        )
    except Exception:
        pass


def _send_contact_confirmation(data):
    """Send confirmation email to the person who contacted us."""
    try:
        send_mail(
            subject="We received your message — Code Yari",
            message=f"Hi {data['name']},\n\nThank you for reaching out to Code Yari!\n\nWe've received your message and will get back to you within 24 hours.\n\nBest regards,\nCode Yari Team\nhello@codeyari.com",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[data['email']],
            fail_silently=True,
        )
    except Exception:
        pass
