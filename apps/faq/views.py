"""FAQ views"""
from django.shortcuts import render
from .models import FAQ, FAQCategory

def faq_list(request):
    categories = FAQCategory.objects.prefetch_related(
        'faqs'
    ).all()
    # Filter only published FAQs
    faqs_by_category = []
    for cat in categories:
        faqs = cat.faqs.filter(published=True).order_by('order')
        if faqs.exists():
            faqs_by_category.append({'category': cat, 'faqs': faqs})

    uncategorized = FAQ.objects.filter(published=True, category__isnull=True).order_by('order')

    context = {
        'page_title': 'Frequently Asked Questions — Code Yari',
        'meta_description': 'Find answers to common questions about Code Yari\'s web development, SEO, app development, pricing and project process.',
        'faqs_by_category': faqs_by_category,
        'uncategorized': uncategorized,
    }
    return render(request, 'faq/list.html', context)
