"""Portfolio views"""
from django.shortcuts import render, get_object_or_404
from .models import PortfolioProject, PortfolioCategory


def portfolio_list(request):
    category_slug = request.GET.get('category')
    projects = PortfolioProject.objects.filter(published=True).select_related('category')
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
    """Case Studies page matching official agency showcase design"""
    case_studies = [
        {
            'title': 'Job Portal Web Application',
            'slug': 'job-portal-web-application',
            'category': 'Web Development',
            'category_slug': 'web-development',
            'category_badge': 'badge-blue',
            'description': 'A role-based platform connecting recruiters and students with job opportunities.',
            'image': 'images/portfolio/case_job_portal.png',
            'tech_tags': [
                {'name': 'React', 'color': '#00D8FF', 'icon': 'bi-atom'},
                {'name': 'Node.js', 'color': '#22C55E', 'icon': 'bi-hexagon-fill'},
                {'name': 'MongoDB', 'color': '#10B981', 'icon': 'bi-database-fill'},
                {'name': 'Tailwind', 'color': '#38BDF8', 'icon': 'bi-wind'},
            ],
            'detail_url': '#',
        },
        {
            'title': 'Hotel Booking Web Application',
            'slug': 'hotel-booking-web-application',
            'category': 'Web Development',
            'category_slug': 'web-development',
            'category_badge': 'badge-blue',
            'description': 'Book your favorite stays with ease. Search, filter, review and explore hotels worldwide.',
            'image': 'images/portfolio/case_hotel_booking.png',
            'tech_tags': [
                {'name': 'HTML', 'color': '#EA580C', 'icon': 'bi-filetype-html'},
                {'name': 'CSS', 'color': '#2563EB', 'icon': 'bi-filetype-css'},
                {'name': 'JavaScript', 'color': '#EAB308', 'icon': 'bi-filetype-js'},
                {'name': 'Node.js', 'color': '#22C55E', 'icon': 'bi-hexagon-fill'},
            ],
            'detail_url': '#',
        },
        {
            'title': 'Meesho Clone (E-Commerce)',
            'slug': 'meesho-clone-ecommerce',
            'category': 'E-Commerce',
            'category_slug': 'e-commerce',
            'category_badge': 'badge-purple',
            'description': 'A full-featured e-commerce platform with product listing, cart, and secure checkout.',
            'image': 'images/portfolio/case_meesho_clone.png',
            'tech_tags': [
                {'name': 'React', 'color': '#00D8FF', 'icon': 'bi-atom'},
                {'name': 'Node.js', 'color': '#22C55E', 'icon': 'bi-hexagon-fill'},
                {'name': 'MongoDB', 'color': '#10B981', 'icon': 'bi-database-fill'},
                {'name': 'Express', 'color': '#94A3B8', 'icon': 'bi-cpu-fill'},
            ],
            'detail_url': '#',
        },
        {
            'title': 'AI Resume Builder',
            'slug': 'ai-resume-builder',
            'category': 'Web Development',
            'category_slug': 'web-development',
            'category_badge': 'badge-blue',
            'description': 'Create professional resumes with the power of AI in just a few clicks.',
            'image': 'images/portfolio/case_ai_resume.png',
            'tech_tags': [
                {'name': 'React', 'color': '#00D8FF', 'icon': 'bi-atom'},
                {'name': 'Python', 'color': '#3B82F6', 'icon': 'bi-filetype-py'},
                {'name': 'FastAPI', 'color': '#06B6D4', 'icon': 'bi-lightning-charge-fill'},
                {'name': 'Tailwind', 'color': '#38BDF8', 'icon': 'bi-wind'},
            ],
            'detail_url': '#',
        },
    ]

    filters = [
        {'name': 'All', 'slug': 'all', 'icon': ''},
        {'name': 'Web Development', 'slug': 'web-development', 'icon': 'bi-globe2'},
        {'name': 'App Development', 'slug': 'app-development', 'icon': 'bi-phone'},
        {'name': 'E-Commerce', 'slug': 'e-commerce', 'icon': 'bi-cart3'},
    ]

    context = {
        'page_title': 'Case Studies — Real Projects. Real Solutions. | Code Yari',
        'meta_description': 'Explore how we turn ideas into powerful digital solutions. Real projects and real results crafted by Code Yari.',
        'case_studies': case_studies,
        'filters': filters,
    }
    return render(request, 'portfolio/case_studies.html', context)

