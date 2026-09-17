from django.contrib import admin
from .models import BlogCategory, BlogPost

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'published', 'published_date', 'created_at')
    list_editable = ('published',)
    list_filter = ('published', 'category', 'author', 'created_at')
    search_fields = ('title', 'excerpt', 'content', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-published_date', '-created_at')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Content', {'fields': ('title', 'slug', 'excerpt', 'content', 'featured_image')}),
        ('Classification', {'fields': ('category', 'author', 'tags')}),
        ('Publishing', {'fields': ('published', 'published_date')}),
        ('SEO', {'fields': ('seo_title', 'seo_description', 'og_image'), 'classes': ('collapse',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
