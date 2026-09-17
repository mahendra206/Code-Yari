from django.contrib import admin
from .models import Testimonial

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'company', 'role', 'rating', 'featured', 'published', 'is_demo', 'order')
    list_editable = ('featured', 'published', 'is_demo', 'order')
    list_filter = ('published', 'featured', 'is_demo', 'rating')
    search_fields = ('client_name', 'company', 'testimonial')
    ordering = ('order', '-created_at')
