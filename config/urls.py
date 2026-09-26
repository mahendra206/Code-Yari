"""
Code Yari — Root URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from apps.core.sitemaps import (
    StaticViewSitemap, ServiceSitemap, PortfolioSitemap, BlogSitemap
)
from apps.portfolio import views as views_portfolio

# Customize admin site
admin.site.site_header = "Code Yari Admin"
admin.site.site_title = "Code Yari Management"
admin.site.index_title = "Welcome to Code Yari Dashboard"

sitemaps = {
    'static': StaticViewSitemap,
    'services': ServiceSitemap,
    'portfolio': PortfolioSitemap,
    'blog': BlogSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),

    # App URLs
    path('', include('apps.core.urls', namespace='core')),
    path('services/', include('apps.services.urls', namespace='services')),
    path('portfolio/', include('apps.portfolio.urls', namespace='portfolio')),
    path('case-studies/', views_portfolio.case_studies_view, name='case_studies'),
    path('blog/', include('apps.blog.urls', namespace='blog')),
    path('faq/', include('apps.faq.urls', namespace='faq')),
    path('leads/', include('apps.leads.urls', namespace='leads')),
    path('testimonials/', include('apps.testimonials.urls', namespace='testimonials')),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),

    # SEO
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', include('apps.core.robots_urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
