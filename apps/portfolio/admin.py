from django.contrib import admin
from .models import PortfolioCategory, PortfolioProject, PortfolioImage

class PortfolioImageInline(admin.TabularInline):
    model = PortfolioImage
    extra = 2
    fields = ('image', 'caption', 'order')

@admin.register(PortfolioCategory)
class PortfolioCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(PortfolioProject)
class PortfolioProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'featured', 'published', 'is_demo', 'completion_date')
    list_editable = ('featured', 'published', 'is_demo')
    list_filter = ('published', 'featured', 'is_demo', 'category')
    search_fields = ('name', 'client_name', 'short_description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [PortfolioImageInline]
    ordering = ('-completion_date', '-created_at')
    fieldsets = (
        ('Project Info', {'fields': ('name', 'slug', 'category', 'client_name', 'short_description', 'full_description')}),
        ('Media', {'fields': ('featured_image',)}),
        ('Technical', {'fields': ('technologies', 'project_url', 'github_url', 'completion_date')}),
        ('Settings', {'fields': ('featured', 'published', 'is_demo')}),
        ('SEO', {'fields': ('seo_title', 'seo_description'), 'classes': ('collapse',)}),
    )
