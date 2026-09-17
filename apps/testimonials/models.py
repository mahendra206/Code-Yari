"""
Testimonials app — Models
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Testimonial(models.Model):
    """Client testimonial — clearly marked demo content during development."""
    client_name = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=100, blank=True)
    testimonial = models.TextField()
    profile_image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    rating = models.PositiveSmallIntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    is_demo = models.BooleanField(
        default=True,
        help_text='Mark as demo content — shown with a demo indicator'
    )
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'

    def __str__(self):
        return f'{self.client_name} — {self.company or "Client"}'

    @property
    def star_range(self):
        return range(self.rating)

    @property
    def empty_star_range(self):
        return range(5 - self.rating)

    @property
    def quote(self):
        return self.testimonial

    @property
    def client_role(self):
        return self.role

    @property
    def client_company(self):
        return self.company

    @property
    def client_image(self):
        return self.profile_image
