"""
Core app models — SiteSettings, TeamMember, StatItem, ContactMessage
"""
from django.db import models
from django.utils import timezone


class SiteSettings(models.Model):
    """Singleton model for site-wide settings manageable from admin."""
    site_name = models.CharField(max_length=100, default='Code Yari')
    tagline = models.CharField(max_length=200, default='Code. Create. Grow.')
    alt_tagline = models.CharField(
        max_length=300,
        default='Sirf code nahi, Yari ke saath solution.',
        blank=True
    )
    logo_text = models.CharField(max_length=50, default='</> Code Yari')
    email = models.EmailField(default='hello@codeyari.com')
    phone = models.CharField(max_length=20, default='+91 98765 43210')
    phone_display = models.CharField(max_length=30, default='+91 98765-43210', blank=True)
    whatsapp = models.CharField(max_length=20, blank=True, help_text='WhatsApp number with country code')
    address = models.TextField(blank=True, default='India')
    city = models.CharField(max_length=100, blank=True, default='India')

    # Social media
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    github = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    facebook = models.URLField(blank=True)

    # SEO / OG
    meta_description = models.TextField(
        max_length=300,
        default='Code Yari — A young digital technology team providing websites, apps, SEO, digital marketing, UI/UX, AI and automation solutions.'
    )
    og_image = models.ImageField(upload_to='seo/', blank=True, null=True)

    # Business hours
    business_hours = models.CharField(max_length=200, blank=True, default='Mon–Sat, 10AM–7PM IST')

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return f'{self.site_name} Settings'

    def save(self, *args, **kwargs):
        # Singleton: only one settings object
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class StatItem(models.Model):
    """Homepage trust statistics — manageable from admin."""
    label = models.CharField(max_length=100, help_text='e.g. Projects Completed')
    value = models.CharField(max_length=20, help_text='e.g. 50+ or 3 Years')
    icon = models.CharField(max_length=50, blank=True, help_text='Bootstrap icon class, e.g. bi-check-circle')
    note = models.CharField(max_length=100, blank=True, help_text='Optional footnote, e.g. (Demo Data)')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Stat Item'
        verbose_name_plural = 'Stat Items'

    def __str__(self):
        return f'{self.value} — {self.label}'


class TeamMember(models.Model):
    """Team member profile manageable from admin."""
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='team/', blank=True, null=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    github = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Team Member'
        verbose_name_plural = 'Team Members'

    def __str__(self):
        return f'{self.name} — {self.role}'


class ContactMessage(models.Model):
    """Contact form submissions."""
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('archived', 'Archived'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    notes = models.TextField(blank=True, help_text='Internal admin notes')
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f'{self.name} — {self.subject} ({self.created_at.strftime("%d %b %Y")})'
