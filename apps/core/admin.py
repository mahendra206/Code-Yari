"""
Core app — Admin configuration
"""
from django.contrib import admin
from .models import SiteSettings, StatItem, TeamMember, ContactMessage


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Branding', {
            'fields': ('site_name', 'tagline', 'alt_tagline', 'logo_text')
        }),
        ('Contact Info', {
            'fields': ('email', 'phone', 'phone_display', 'whatsapp', 'address', 'city', 'business_hours')
        }),
        ('Social Media', {
            'fields': ('linkedin', 'twitter', 'instagram', 'github', 'youtube', 'facebook'),
            'classes': ('collapse',)
        }),
        ('SEO', {
            'fields': ('meta_description', 'og_image'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        # Singleton — prevent creating multiple instances
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(StatItem)
class StatItemAdmin(admin.ModelAdmin):
    list_display = ('label', 'value', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    ordering = ('order',)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    ordering = ('order', 'name')
    search_fields = ('name', 'role')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'phone', 'subject', 'message', 'ip_address', 'created_at')
    list_editable = ('status',)
    ordering = ('-created_at',)
    fieldsets = (
        ('Message Details', {
            'fields': ('name', 'email', 'phone', 'subject', 'message', 'ip_address', 'created_at')
        }),
        ('Admin', {
            'fields': ('status', 'notes')
        }),
    )
