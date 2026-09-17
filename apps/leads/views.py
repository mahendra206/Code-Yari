"""Leads / Quote Request form and views"""
from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Lead


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            'name', 'email', 'phone', 'company',
            'service', 'budget', 'project_type',
            'project_description', 'deadline', 'preferred_contact',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name', 'id': 'quote-name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com', 'id': 'quote-email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 98765 43210', 'id': 'quote-phone'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company / Business Name (optional)', 'id': 'quote-company'}),
            'service': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Web Development, SEO, App Development', 'id': 'quote-service'}),
            'budget': forms.Select(attrs={'class': 'form-select', 'id': 'quote-budget'}),
            'project_type': forms.Select(attrs={'class': 'form-select', 'id': 'quote-type'}),
            'project_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Describe your project, goals, and any specific requirements...', 'id': 'quote-description'}),
            'deadline': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. ASAP, 2 months, end of year', 'id': 'quote-deadline'}),
            'preferred_contact': forms.Select(attrs={'class': 'form-select', 'id': 'quote-contact'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if len(name) < 2:
            raise forms.ValidationError("Please enter your full name.")
        return name

    def clean_project_description(self):
        desc = self.cleaned_data['project_description'].strip()
        if len(desc) < 20:
            raise forms.ValidationError("Please provide more detail about your project.")
        return desc


def get_quote(request):
    initial_service = request.GET.get('service', '')

    if request.method == 'POST':
        # Honeypot check
        if request.POST.get('website'):
            return redirect('leads:get_quote')

        form = QuoteForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.ip_address = _get_client_ip(request)
            lead.save()

            # Send notifications
            _send_lead_notification(lead)
            _send_lead_confirmation(lead)

            messages.success(
                request,
                f"Thank you, {lead.name}! Your quote request has been submitted. We'll get back to you within 24 hours!"
            )
            return redirect('leads:get_quote')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = QuoteForm(initial={'service': initial_service})

    from apps.services.models import Service
    services = Service.objects.filter(is_active=True).values_list('name', flat=True)

    context = {
        'page_title': 'Get a Free Quote — Code Yari',
        'meta_description': 'Request a free project quote from Code Yari. Tell us about your project and we\'ll get back to you within 24 hours.',
        'form': form,
        'services': services,
    }
    return render(request, 'leads/get_quote.html', context)


def _get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def _send_lead_notification(lead):
    try:
        send_mail(
            subject=f"New Quote Request: {lead.service or 'General'} — {lead.name}",
            message=f"New lead from the website!\n\nName: {lead.name}\nEmail: {lead.email}\nPhone: {lead.phone or 'N/A'}\nCompany: {lead.company or 'N/A'}\nService: {lead.service or 'N/A'}\nBudget: {lead.get_budget_display()}\nProject Type: {lead.get_project_type_display()}\nDeadline: {lead.deadline or 'N/A'}\nPreferred Contact: {lead.get_preferred_contact_display()}\n\nProject Description:\n{lead.project_description}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=True,
        )
    except Exception:
        pass


def _send_lead_confirmation(lead):
    try:
        send_mail(
            subject="Quote Request Received — Code Yari",
            message=f"Hi {lead.name},\n\nThank you for reaching out to Code Yari!\n\nWe've received your quote request and our team will review it and get back to you within 24 hours.\n\nProject: {lead.service or 'Digital Solution'}\nBudget Range: {lead.get_budget_display()}\n\nBest regards,\nCode Yari Team\nhello@codeyari.com",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[lead.email],
            fail_silently=True,
        )
    except Exception:
        pass
