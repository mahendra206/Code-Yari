"""
Core app — Sitemaps
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.services.models import Service
from apps.portfolio.models import PortfolioProject
from apps.blog.models import BlogPost


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return [
            'core:home', 'core:about', 'core:team', 'core:contact',
            'leads:get_quote', 'services:list', 'portfolio:list',
            'blog:list', 'faq:list', 'testimonials:list',
            'core:privacy_policy', 'core:terms'
        ]

    def location(self, item):
        return reverse(item)


class ServiceSitemap(Sitemap):
    priority = 0.8
    changefreq = 'monthly'
    protocol = 'https'

    def items(self):
        return Service.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class PortfolioSitemap(Sitemap):
    priority = 0.7
    changefreq = 'monthly'
    protocol = 'https'

    def items(self):
        return PortfolioProject.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.updated_at


class BlogSitemap(Sitemap):
    priority = 0.7
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return BlogPost.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.updated_at
