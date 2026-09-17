"""Testimonials views"""
from django.shortcuts import render
from .models import Testimonial

def testimonials_list(request):
    testimonials = Testimonial.objects.filter(published=True).order_by('order', '-created_at')
    context = {
        'page_title': 'Client Testimonials — Code Yari',
        'meta_description': 'Read what our clients say about working with Code Yari for web development, SEO, digital marketing and more.',
        'testimonials': testimonials,
    }
    return render(request, 'testimonials/list.html', context)
