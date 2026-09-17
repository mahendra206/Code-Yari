"""Services views"""
from django.shortcuts import render, get_object_or_404
from .models import Service


def services_list(request):
    services = Service.objects.filter(is_active=True).order_by('order')
    featured = services.filter(is_featured=True)
    context = {
        'page_title': 'Our Services — Code Yari',
        'meta_description': 'Explore Code Yari\'s full range of digital services: web development, app development, SEO, digital marketing, UI/UX, AI automation, and more.',
        'services': services,
        'featured_services': featured,
    }
    return render(request, 'services/list.html', context)


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    related_services = Service.objects.filter(
        is_active=True
    ).exclude(pk=service.pk).order_by('order')[:4]
    context = {
        'page_title': service.get_seo_title(),
        'meta_description': service.get_seo_description(),
        'service': service,
        'related_services': related_services,
        'features': service.features if isinstance(service.features, list) else [],
        'technologies': service.technologies if isinstance(service.technologies, list) else [],
    }
    return render(request, 'services/detail.html', context)
