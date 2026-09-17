"""
Services app — Models
"""
import json
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Service(models.Model):
    """Digital service offered by Code Yari."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.CharField(max_length=300)
    full_description = models.TextField()
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text='Bootstrap Icons class, e.g. bi-code-slash'
    )
    featured_image = models.ImageField(upload_to='services/', blank=True, null=True)

    # JSON fields for structured data
    features = models.JSONField(
        default=list, blank=True,
        help_text='List of feature strings, e.g. ["Responsive Design", "SEO Ready"]'
    )
    technologies = models.JSONField(
        default=list, blank=True,
        help_text='List of technology strings, e.g. ["Django", "React", "PostgreSQL"]'
    )

    # Flags
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    # SEO
    seo_title = models.CharField(max_length=70, blank=True)
    seo_description = models.CharField(max_length=160, blank=True)
    og_image = models.ImageField(upload_to='services/og/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', 'is_featured']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('services:detail', kwargs={'slug': self.slug})

    def get_seo_title(self):
        return self.seo_title or f'{self.name} — Code Yari'

    def get_seo_description(self):
        return self.seo_description or self.short_description

    def get_theme(self):
        theme_map = {
            'web-development': 'theme-blue',
            'app-development': 'theme-green',
            'seo-google-ranking': 'theme-orange',
            'digital-marketing': 'theme-purple',
            'uiux-design': 'theme-pink',
            'ai-automation': 'theme-cyan',
            'e-commerce-development': 'theme-blue',
            'website-maintenance': 'theme-green',
            'hosting-deployment': 'theme-cyan',
            'custom-software-development': 'theme-purple',
            'website-speed-optimization': 'theme-orange',
            'content-seo-writing': 'theme-pink',
        }
        return theme_map.get(self.slug, 'theme-blue')

    def get_illustration(self):
        ill_map = {
            'web-development': 'images/services/ill_web_dev.png',
            'app-development': 'images/services/ill_app_dev.png',
            'seo-google-ranking': 'images/services/ill_seo.png',
            'digital-marketing': 'images/services/ill_marketing.png',
            'uiux-design': 'images/services/ill_uiux.png',
            'ai-automation': 'images/services/ill_ai.png',
            'e-commerce-development': 'images/services/ill_web_dev.png',
            'website-maintenance': 'images/services/ill_app_dev.png',
            'hosting-deployment': 'images/services/ill_ai.png',
            'custom-software-development': 'images/services/ill_web_dev.png',
            'website-speed-optimization': 'images/services/ill_seo.png',
            'content-seo-writing': 'images/services/ill_marketing.png',
        }
        return ill_map.get(self.slug, 'images/services/ill_web_dev.png')
