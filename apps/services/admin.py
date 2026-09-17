from django.contrib import admin
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_featured', 'is_active', 'order', 'updated_at')
    list_editable = ('is_featured', 'is_active', 'order')
    list_filter = ('is_active', 'is_featured')
    search_fields = ('name', 'short_description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')
    fieldsets = (
        ('Basic Info', {'fields': ('name', 'slug', 'short_description', 'full_description', 'icon', 'featured_image')}),
        ('Details', {'fields': ('features', 'technologies')}),
        ('Settings', {'fields': ('is_featured', 'is_active', 'order')}),
        ('SEO', {'fields': ('seo_title', 'seo_description', 'og_image'), 'classes': ('collapse',)}),
    )
