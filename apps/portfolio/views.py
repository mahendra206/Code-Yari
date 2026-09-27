"""Portfolio views"""
from django.shortcuts import render, get_object_or_404
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
    """Case Studies page matching official agency showcase design"""
    case_studies = [
        {
            'title': 'TeachMANTRA — Student Academy & Test Portal',
            'slug': 'teachmantra-student-academy-test-portal',
            'category': 'Web Development',
            'category_slug': 'web-development',
            'category_badge': 'badge-amber',
            'theme_class': 'theme-amber',
            'metric': '10,000+ Students • Syllabus & Mock Tests',
            'metric_class': 'metric-amber',
            'metric_icon': 'bi-mortarboard-fill',
            'description': 'A comprehensive online learning academy portal featuring course syllabus downloads, live mock tests, student registration, and certificate verification.',
            'image': 'images/portfolio/teachmantra_cover.jpg',
            'tech_tags': [
                {'name': 'Python', 'color': '#3B82F6', 'icon': 'bi-filetype-py', 'chip_class': 'chip-amber'},
                {'name': 'Django', 'color': '#10B981', 'icon': 'bi-layers-half', 'chip_class': 'chip-amber'},
                {'name': 'Bootstrap', 'color': '#8B5CF6', 'icon': 'bi-bootstrap-fill', 'chip_class': 'chip-amber'},
                {'name': 'JavaScript', 'color': '#F59E0B', 'icon': 'bi-filetype-js', 'chip_class': 'chip-amber'},
            ],
            'detail_url': '/portfolio/teachmantra-student-academy-test-portal/',
            'project_url': 'https://www.theteachmantra.com/',
            'live_label': 'Live Portal',
            'badge_dot_class': 'dot-amber',
            'explore_btn_class': 'btn-explore-amber',
        },
        {
            'title': 'NEXPLAY — Gaming Ecosystem & Setup Builder',
            'slug': 'nexplay-gaming-ecosystem-setup-builder',
            'category': 'E-Commerce',
            'category_slug': 'e-commerce',
            'category_badge': 'badge-purple',
            'theme_class': 'theme-purple',
            'metric': '3.5x Faster Builder • Custom Battlestations',
            'metric_class': 'metric-purple',
            'metric_icon': 'bi-controller',
            'description': 'An interactive gaming ecosystem and custom PC setup builder featuring personalized playstyle recommendations, hardware configurations, and esports peripherals.',
            'image': 'images/portfolio/nexplay_cover.jpg',
            'tech_tags': [
                {'name': 'React', 'color': '#00D8FF', 'icon': 'bi-browser-chrome', 'chip_class': 'chip-purple'},
                {'name': 'Vite', 'color': '#A855F7', 'icon': 'bi-lightning-charge-fill', 'chip_class': 'chip-purple'},
                {'name': 'Tailwind', 'color': '#38BDF8', 'icon': 'bi-wind', 'chip_class': 'chip-purple'},
                {'name': '3D Rig', 'color': '#EC4899', 'icon': 'bi-cpu', 'chip_class': 'chip-purple'},
            ],
            'detail_url': '/portfolio/nexplay-gaming-ecosystem-setup-builder/',
            'project_url': 'https://nexplay-hub.netlify.app/',
            'live_label': 'Live Rig Builder',
            'badge_dot_class': 'dot-purple',
            'explore_btn_class': 'btn-explore-purple',
        },
        {
            'title': 'Houzez — Luxury Real Estate & Property Marketplace',
            'slug': 'houzez-luxury-real-estate-property-marketplace',
            'category': 'E-Commerce',
            'category_slug': 'e-commerce',
            'category_badge': 'badge-emerald',
            'theme_class': 'theme-emerald',
            'metric': '$14M+ Luxury Listings • Real-time Filter',
            'metric_class': 'metric-emerald',
            'metric_icon': 'bi-buildings-fill',
            'description': 'A modern real estate marketplace platform featuring luxury property listings for sale & rent, interactive filter search, realtor directories, and listing inquiries.',
            'image': 'images/portfolio/houzez_cover.jpg',
            'tech_tags': [
                {'name': 'React', 'color': '#00D8FF', 'icon': 'bi-browser-chrome', 'chip_class': 'chip-emerald'},
                {'name': 'Tailwind', 'color': '#38BDF8', 'icon': 'bi-wind', 'chip_class': 'chip-emerald'},
                {'name': 'Map Filter', 'color': '#10B981', 'icon': 'bi-geo-alt-fill', 'chip_class': 'chip-emerald'},
                {'name': 'Verified', 'color': '#06B6D4', 'icon': 'bi-shield-check', 'chip_class': 'chip-emerald'},
            ],
            'detail_url': '/portfolio/houzez-luxury-real-estate-property-marketplace/',
            'project_url': 'https://houzez-1.netlify.app/',
            'live_label': 'Live Marketplace',
            'badge_dot_class': 'dot-emerald',
            'explore_btn_class': 'btn-explore-emerald',
        },
        {
            'title': 'ResumeAI — AI Resume Builder & ATS Studio',
            'slug': 'resumeai-ai-resume-builder-ats-studio',
            'category': 'Web Development',
            'category_slug': 'web-development',
            'category_badge': 'badge-cyan',
            'theme_class': 'theme-cyan',
            'metric': '98% ATS Score • Instant A4 Preview',
            'metric_class': 'metric-cyan',
            'metric_icon': 'bi-stars',
            'description': 'An intelligent AI-powered resume builder featuring real-time ATS optimization, instant A4 preview, dynamic color themes, and one-click PDF export.',
            'image': 'images/portfolio/resume_ai_cover.jpg',
            'tech_tags': [
                {'name': 'AI Engine', 'color': '#06B6D4', 'icon': 'bi-robot', 'chip_class': 'chip-cyan'},
                {'name': 'PDF Export', 'color': '#EF4444', 'icon': 'bi-file-earmark-pdf-fill', 'chip_class': 'chip-cyan'},
                {'name': 'ATS Scoring', 'color': '#3B82F6', 'icon': 'bi-lightning-charge-fill', 'chip_class': 'chip-cyan'},
                {'name': 'Multi-Theme', 'color': '#8B5CF6', 'icon': 'bi-palette-fill', 'chip_class': 'chip-cyan'},
            ],
            'detail_url': '/portfolio/resumeai-ai-resume-builder-ats-studio/',
            'project_url': 'https://resumebulider-ai.netlify.app/',
            'live_label': 'Live Studio',
            'badge_dot_class': 'dot-cyan',
            'explore_btn_class': 'btn-explore-cyan',
        },
    ]

    filters = [
        {'name': 'All', 'slug': 'all', 'icon': ''},
        {'name': 'Web Development', 'slug': 'web-development', 'icon': 'bi-globe2'},
        {'name': 'E-Commerce', 'slug': 'e-commerce', 'icon': 'bi-cart3'},
        {'name': 'Mobile App', 'slug': 'app-development', 'icon': 'bi-phone'},
    ]

    context = {
        'page_title': 'Case Studies — Real Projects. Real Solutions. | Code Yari',
        'meta_description': 'Explore how we turn ideas into powerful digital solutions. Real projects and real results crafted by Code Yari.',
        'case_studies': case_studies,
        'filters': filters,
    }
    return render(request, 'portfolio/case_studies.html', context)

