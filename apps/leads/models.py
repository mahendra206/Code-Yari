"""
Leads app — Models (Quote Requests)
"""
from django.db import models
from django.utils import timezone


class Lead(models.Model):
    """Quote/project inquiry submitted by a potential client."""

    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('in_discussion', 'In Discussion'),
        ('proposal_sent', 'Proposal Sent'),
        ('won', 'Won'),
        ('lost', 'Lost'),
        ('completed', 'Completed'),
    ]

    BUDGET_CHOICES = [
        ('under_10k', 'Under ₹10,000'),
        ('10k_25k', '₹10,000 – ₹25,000'),
        ('25k_50k', '₹25,000 – ₹50,000'),
        ('50k_1l', '₹50,000 – ₹1,00,000'),
        ('1l_3l', '₹1,00,000 – ₹3,00,000'),
        ('above_3l', 'Above ₹3,00,000'),
        ('discuss', 'Let\'s Discuss'),
    ]

    CONTACT_METHOD_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone Call'),
        ('whatsapp', 'WhatsApp'),
        ('video_call', 'Video Call'),
    ]

    PROJECT_TYPE_CHOICES = [
        ('new', 'New Project'),
        ('redesign', 'Redesign / Revamp'),
        ('maintenance', 'Maintenance / Updates'),
        ('consulting', 'Consulting / Strategy'),
        ('other', 'Other'),
    ]

    # Client info
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=100, blank=True)

    # Project details
    service = models.CharField(max_length=100, blank=True, help_text='Which service are you interested in?')
    budget = models.CharField(max_length=20, choices=BUDGET_CHOICES, blank=True)
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPE_CHOICES, blank=True)
    project_description = models.TextField()
    deadline = models.CharField(max_length=100, blank=True, help_text='e.g. ASAP, 3 months, flexible')
    preferred_contact = models.CharField(max_length=20, choices=CONTACT_METHOD_CHOICES, default='email')

    # CRM
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    notes = models.TextField(blank=True, help_text='Internal notes (not shown to client)')
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Lead / Quote Request'
        verbose_name_plural = 'Leads / Quote Requests'

    def __str__(self):
        return f'{self.name} — {self.service or "General"} ({self.get_status_display()})'

    def get_status_color(self):
        colors = {
            'new': 'primary',
            'contacted': 'info',
            'in_discussion': 'warning',
            'proposal_sent': 'secondary',
            'won': 'success',
            'lost': 'danger',
            'completed': 'dark',
        }
        return colors.get(self.status, 'secondary')
