"""Portfolio views"""
from django.shortcuts import render, get_object_or_404, redirect
from .models import PortfolioProject, PortfolioCategory


from django.db.models import Case, When, Value, IntegerField


def portfolio_list(request):
    category_slug = request.GET.get('category')
    
    # Priority ordering: TeachMANTRA (1), NEXPLAY (2), Houzez (3), ResumeAI (4), other real projects (5), demo projects (6)
    order_priority = Case(
        When(slug__icontains='teachmantra', then=Value(1)),
        When(slug__icontains='nexplay', then=Value(2)),
        When(slug__icontains='houzez', then=Value(3)),
        When(slug__icontains='resume', then=Value(4)),
        When(is_demo=False, then=Value(5)),
        default=Value(6),
        output_field=IntegerField()
    )

    projects = PortfolioProject.objects.filter(published=True).select_related('category').annotate(
        priority=order_priority
    ).order_by('priority', 'created_at')

    categories = PortfolioCategory.objects.all()
    active_category = None

    if category_slug:
        active_category = get_object_or_404(PortfolioCategory, slug=category_slug)
        projects = projects.filter(category=active_category)

    context = {
        'page_title': 'Our Portfolio — Code Yari',
        'meta_description': 'Explore Code Yari\'s portfolio of websites, apps, SEO projects and digital solutions we\'ve built for our clients.',
        'projects': projects,
        'categories': categories,
        'active_category': active_category,
    }
    return render(request, 'portfolio/list.html', context)


def portfolio_detail(request, slug):
    project = get_object_or_404(PortfolioProject, slug=slug, published=True)
    gallery = project.gallery_images.all()
    related = PortfolioProject.objects.filter(
        published=True, category=project.category
    ).exclude(pk=project.pk)[:3]

    context = {
        'page_title': project.get_seo_title(),
        'meta_description': project.get_seo_description(),
        'project': project,
        'gallery': gallery,
        'related_projects': related,
        'technologies': project.technologies if isinstance(project.technologies, list) else [],
    }
    return render(request, 'portfolio/detail.html', context)


def case_studies_view(request):
    """Case Studies page is now merged into portfolio showcase. Redirect to unified portfolio list."""
    return redirect('portfolio:list', permanent=True)

