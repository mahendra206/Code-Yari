from django.contrib import admin
from .models import FAQCategory, FAQ

@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'published', 'order')
    list_editable = ('published', 'order')
    list_filter = ('published', 'category')
    search_fields = ('question', 'answer')
    ordering = ('order', 'created_at')
