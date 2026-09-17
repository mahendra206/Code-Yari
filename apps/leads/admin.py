from django.contrib import admin
from .models import Lead

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'service', 'budget', 'status', 'created_at')
    list_filter = ('status', 'budget', 'project_type', 'preferred_contact', 'created_at')
    search_fields = ('name', 'email', 'phone', 'company', 'service', 'project_description')
    list_editable = ('status',)
    readonly_fields = ('ip_address', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    fieldsets = (
        ('Client Information', {'fields': ('name', 'email', 'phone', 'company')}),
        ('Project Details', {'fields': ('service', 'budget', 'project_type', 'project_description', 'deadline', 'preferred_contact')}),
        ('CRM', {'fields': ('status', 'notes')}),
        ('System', {'fields': ('ip_address', 'created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    def get_status_color(self, obj):
        return obj.get_status_color()
