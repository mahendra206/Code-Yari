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


from django.utils.html import format_html

from django.urls import reverse

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('photo_preview', 'name', 'role', 'order', 'is_active', 'delete_action')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    ordering = ('order', 'name')
    search_fields = ('name', 'role', 'bio')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'role', 'bio', 'photo')
        }),
        ('Social Links', {
            'fields': ('linkedin', 'twitter', 'github'),
            'description': 'Paste full profile links (e.g., https://linkedin.com/in/username)'
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
    )

    def photo_preview(self, obj):
        url = obj.get_photo_url
        if url:
            return format_html('<img src="{}" style="width: 38px; height: 38px; object-fit: cover; border-radius: 8px; border: 2px solid #e2e8f0;" />', url)
        return format_html('<span style="color: #94a3b8; font-size: 0.8rem;">No photo</span>')
    photo_preview.short_description = 'Photo'

    def delete_action(self, obj):
        delete_url = reverse('admin:core_teammember_delete', args=[obj.pk])
        return format_html(
            '<a href="{}" class="row-delete-btn" title="Delete {}">'
            '🗑️ Delete'
            '</a>',
            delete_url,
            obj.name
        )
    delete_action.short_description = 'Delete'


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
